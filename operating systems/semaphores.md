- A synchronization primitive shaped for problems mutex cannot express: waiting for a resource to exist, signaling an event, counting a pool of available slots.
- Same kernel substrate as the [[locks#Sleep Mutex|sleep mutex]] — wait queues keyed by address — but with different state (a counter, not a boolean) and asymmetric operations: any thread can signal availability, and any thread can wait for it.
- Mutex's wait condition is "the region is occupied." Producer-consumer's wait condition is "the resource does not exist yet." Different shape, different primitive.

# The Lost Wakeup Problem

- DIY bounded-buffer producer-consumer using [[locks#Sleep Mutex|sleep/wakeup]] plus a counter, without semaphores:

```c
#define N 100
int count = 0;

void producer(void) {
    while (1) {
        int item = produce_item();
        if (count == N) sleep(&buffer);     // buffer full
        insert_item(item);
        count++;
        if (count == 1) wakeup(&buffer);    // buffer was empty
    }
}

void consumer(void) {
    while (1) {
        if (count == 0) sleep(&buffer);     // buffer empty
        int item = remove_item();
        count--;
        if (count == N - 1) wakeup(&buffer); // buffer was full
        consume_item(item);
    }
}
```

- The bug:
	1. Consumer reads `count == 0`, decides to sleep.
	2. Consumer is preempted before the `sleep(&buffer)` call.
	3. Producer runs, inserts an item, sees `count == 1`, calls `wakeup(&buffer)`.
	4. The wait queue is empty — no one is sleeping yet — so wakeup does nothing.
	5. Consumer resumes, calls `sleep(&buffer)`, sleeps forever.

- The wakeup was lost in the gap between "decide to sleep" and "actually asleep."
- The fix: take a lock around the condition check and the sleep, and have `sleep` atomically release the lock as it suspends. The producer must hold the same lock to call `wakeup`. If the producer is mid-update when the consumer is about to sleep, it cannot wake until the consumer's `sleep` releases the lock — guaranteeing the wakeup arrives after the sleeper is queued.

# Semaphores

- An integer with two atomic operations. The integer counts pending wakeups (or available slots, depending on framing).

**down(s)** / **P(s)** / **wait(s)**

- If `s > 0`: decrement and return immediately.
- If `s == 0`: block on the semaphore's wait queue. Wake when some other thread calls `up`.

**up(s)** / **V(s)** / **signal(s)**

- Increment `s`. If any thread is blocked on the semaphore, wake one (selection is unspecified; usually FIFO).
- Never blocks. Always returns immediately.

- Both operations are atomic — the OS implements them as system calls, with the increment and the wakeup-decision happening under a kernel lock. The lost-wakeup race is internal and already solved.
- A ==binary semaphore== is a semaphore restricted to {0, 1}. It behaves as a mutex but is not the same object — a binary semaphore can be `up`-ed by a thread that did not `down` it; a mutex cannot.

# Producer-Consumer

- Three semaphores split the responsibilities:
	- `mutex = 1` — mutual exclusion on the buffer (binary).
	- `empty = N` — number of empty slots; producer waits on it.
	- `full = 0` — number of full slots; consumer waits on it.

```c
#define N 100
semaphore mutex = 1;
semaphore empty = N;
semaphore full  = 0;

void producer(void) {
    while (1) {
        int item = produce_item();
        down(&empty);           // wait for an empty slot
        down(&mutex);           // enter critical section
        insert_item(item);
        up(&mutex);             // leave critical section
        up(&full);              // signal a full slot
    }
}

void consumer(void) {
    while (1) {
        down(&full);            // wait for a full slot
        down(&mutex);           // enter critical section
        int item = remove_item();
        up(&mutex);             // leave critical section
        up(&empty);             // signal an empty slot
        consume_item(item);
    }
}
```

- `down(&empty)` and `down(&full)` are *outside* `down(&mutex)`. If the producer took the buffer mutex first and only then noticed the buffer was full, it would sleep with the mutex held — and the consumer could never enter to drain it. A [[deadlocks|deadlock]].
- The atomicity of `down`/`up` removes the lost-wakeup hazard: the producer's `up(&full)` either finds a queued consumer (wakes it) or increments the count (the next `down(&full)` decrements without sleeping).

# Barriers

- A barrier holds the first $N - 1$ arriving threads until the $N$-th arrives, then releases all $N$ at once. Used to separate phases of a parallel algorithm.
- Example: parallel matrix multiplication $M_n = M_{n-1} \times C$. Each thread computes one submatrix of $M_n$. None can start the next iteration until every thread has finished the current one.

```
phase 1:           phase 2:           phase 3:

A ----+            A ----+ ----+      A ---- ====+
B ----+            B ====+ ----+      B ---- ====+
C ----+            C ----+ ====+      C ---- ----+
D --==+            D ====+ ====+      D ---- ====+
      |                                          |
   Barrier            Barrier               Released
```

- Implementation: a counter (initially 0) protected by a mutex, plus a semaphore the threads sleep on. Each arrival increments the counter; the $N$-th arrival calls `up` $N - 1$ times to release the rest.
- pthread provides `pthread_barrier_t` directly; the join-on-N-threads idiom (`pthread_join` in a loop) is the same primitive at coarser granularity.

# Readers-Writers

- Multiple threads may read a shared structure simultaneously; a write requires exclusive access. The asymmetric pattern below is the canonical solution.

```c
semaphore mutex = 1;     // protects rc
semaphore db = 1;        // exclusive lock on the database
int rc = 0;              // number of active readers

void reader(void) {
    while (1) {
        down(&mutex);
        rc++;
        if (rc == 1) down(&db);   // first reader acquires db
        up(&mutex);

        read_data_base();

        down(&mutex);
        rc--;
        if (rc == 0) up(&db);     // last reader releases db
        up(&mutex);
        use_data_read();
    }
}

void writer(void) {
    while (1) {
        think_up_data();
        down(&db);
        write_data_base();
        up(&db);
    }
}
```

- The first reader acquires `db` on behalf of all readers; the last reader releases it. Subsequent readers only touch `rc`.
- Writers contend for `db` directly. If a reader holds `db`, the writer blocks until the reader count drops to zero.
- ==Writer starvation==: a continuous stream of readers can keep `rc > 0` forever, locking writers out indefinitely. Variants give writers priority by adding a third semaphore that readers must `down` after a writer arrives.

# Read-Copy-Update

- A pattern for data structures with frequent reads and rare writes. Readers run lock-free; the writer publishes a new version atomically and only frees the old version once no reader can still observe it.
- Update protocol on a tree, replacing subtree rooted at parent's child:
	1. Allocate and fully initialize the new subtree.
	2. Atomically swap the parent's child pointer from old to new. Future readers see the new tree; in-flight readers still hold pointers into the old tree.
	3. Wait until every reader that started before the swap has finished its read.
	4. Free the old subtree.

- Step 3 needs a way to know when in-flight readers are done. RCU adds a ==read-side critical section== API that readers must enter before reading and exit after. The writer's wait is "until every reader who entered before the swap has exited" — sometimes implemented as "wait for every CPU to context-switch at least once."
- Not mutual exclusion — readers and writer run concurrently. The cost: readers may briefly see a stale version. Right when stale reads are tolerable; wrong when they're not.
- Avoids the writer starvation and lock contention of [[#Readers-Writers|readers-writers]] by removing the lock entirely on the read path.

[[concurrency]]