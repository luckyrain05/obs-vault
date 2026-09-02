- [[concurrency#Critical Section|Mutual exclusion]] mechanisms.
- A ==lock== guards a [[concurrency#Critical Section|critical section]] so at most one thread executes inside it at a time.

# Interrupt Lock

- On a single [[cpu#Cores|core]], the only way for [[threads]] inside a [[concurrency#Critical Section|critical section]] to corrupt data is [[schedulers#Preemption|preemption]] from a scheduler, which will halt the [[processes|process]] via a hardware interrupt.
- Thus, we simply lock interrupts on entry into the critical section, and unlock on exit.

```c
lock()   { disable_interrupt(); }
unlock() { enable_interrupt(); }
```

- However, the interrupt does not communicate across other cores, it only stops the scheduler of the same core from interrupting itself. 
- Thus, multiple cores can still enter the same critical region.

# Lock Variable Algorithm

- We can try introducing a [[memory#Globals|global]] integer variable shared across all cores. 
- `locked` ∈ {0, 1}.

```c
void acquire(struct spinlock *lk) {
    for (;;) {
        if (!lk->locked) {
            lk->locked = 1;
            lock();
            break;
        }
    }
}

void release(struct spinlock *lk) {
	lk->locked = 0;
	unlock();
}
```

- A shared variable tells one thread if another is in the critical section, and waits inside `acquire()`'s for loop until the variable `lk` to equal to `0`.
- `lk -> locked = 1` is [[concurrency#Atomicness|atomic]], compiles to one instruction: `mov [locked], 1`.
- However, this is even worse than the simple interrupt lock above.
	- One thread can still read `0` before the other has updated `locked`, and enter into the critical section concurrently. Fails at both single and multi-core processing.
	- Essentially creating a [[pipelining#Hazards|write-after-read]] data hazard.

# Peterson's Algorithm

- Can enforce [[concurrency#Critical Section|mutual exclusion]] for up to 2 [[threads]] with any cores, assigned $0$ and $1$.
- Declare 2 [[memory#compilers Compile Time vs Runtime Compile-Time Allocations|global]] variables.
	- An [[arrays|array]] `intent[]`with 2 indexes to track the intent of both threads. `1`, or true, for intent to entry. `0`, or false, if otherwise. 
	- An integer `turn` storing `0` or `1`, representing either thread's turn.
- Since we assigned our threads $0$ and $1$, their numbers also works as their designated index in the array. `intent[1]`'s value represents thread $1$'s intent, etc.
- Upon entry, we write to our index first, before checking if the other thread's intent.

```c
bool intent[2];
int turn;

void enter_region(int process) {
    intent[process] = 1;     
    turn = 1 - process;
    while (intent[other] && turn == other);
}

void leave_region(int process) {
    intent[process] = false;
}
```

- Peterson's solves lock variable's [[pipelining#Hazards|write-after-read]] data hazard by reading after write. It is impossible to read a stale variable since the read will always happen after.
- The `turn` variable is used to solve any [[deadlocks]].
	- Suppose `t1` intents to enter and `t2` declares intent before `t1` does enter, `intent[other]` will return true for both threads indefinitely.
	- The `turn` variable can only be `0` or `1`, giving the right of way to whoever that bit is flipped to.
- Does not work for thread counts $> 2$.

# [[concurrency#Atomicness|Atomic]] Operations

- [[x86 assembly]] offers special atomic variants of otherwise non-atomic operations.
- Specifically made to address the data hazards and race conditions of locks.
	- Implemented through dedicated circuitry, the core will physically hoard the [[cpu#Bus|memory bus]] until these operations complete. 
	- Thus the RAW data hazard is a physical impossibility.

**TSL**

- ==Test and set lock==.
- `TSL REG, LOCK`
	- Atomically writes `*LOCK` into `REG`, then writes a nonzero value into `*LOCK`. 
	- The read and the write happens in one [[cpu#The clock|clock cycle]].

**XCHG**

- ==Exchange==.
- `xchg REG, MEM`
	- Atomically swap register and memory. 
	- Preload the register with a non-zero value, then it is identical to `TSL`.

**CAS** 

- ==Compare and swap==.
- `CAS(addr, expected, new)`
	- If `*addr == expected`, store `new` and return `expected`
	- Else return the current `*addr`.
- Strictly more expressive than TSL. A thread can act only when memory is in a known state, which builds lock-free data structures.

# Spinlock

- Lock variable algorithm glowed up with `TSL`.

```nasm
acquire:
    TSL REG, LOCK     ; copy LOCK into REG, then set LOCK to > 0
    CMP REG, #0       ; was it locked?
    JNE acquire       ; stall and wait if locked
    RET               ; was unlocked, continue

release:
    MOVE LOCK, #0
    RET
```

- xv6's version uses `xchg`:

```c
while (xchg(&lk->locked, 1) != 0) ;
```

- Since `TSL` is atomic, it is impossible for another thread to read `LOCK` before it gets updated.
- Works for any number of cores or threads.
- However, cores awaiting entry essentially stalls and wastes time.

# Mutex

- A spinlock that repurposes the core instead of stalling until entry.
- Hands control to the [[schedulers|scheduler]].

```nasm
mutex_lock:
    TSL REG, MUTEX
    CMP REG, #0
    JZE entrance
    CALL thread_yield ; locked, let scheduler repurpose the core.
    JMP mutex_lock    ; re-enter when scheduled again
entrance:
    RET

mutex_unlock:
    MOVE MUTEX, #0
    RET
```

# Sleep Mutex

- The yield-mutex still wastes scheduler cycles. After `thread_yield` the waiter goes back on the run queue marked runnable; the scheduler has no idea it's only waiting for `MUTEX` to flip and keeps picking it. Every pick re-runs `TSL`, finds the lock held, yields again.
- Take the waiter off the run queue entirely until the holder releases. Block, don't retry.

**sleep / wakeup**

- Kernel primitives that change a thread's scheduler state. ==chan== is an address used as a tag; the kernel keeps wait queues keyed by `chan`, typically as a hash table.

```c
sleep(void *chan);     // runnable to blocked, tagged with chan
wakeup(void *chan);    // every thread blocked on chan to runnable
```

- Different `chan` values isolate waiters — a thread blocked on `&LOCK_A` is on a different queue from one blocked on `&LOCK_B` or `&disk_buffer`. `wakeup(&LOCK_A)` walks only the queue for that key.

**Acquire / release**

- Acquire: `TSL`; on failure, `sleep(&MUTEX)`. Release: clear the byte, `wakeup(&MUTEX)`.
- The waiter is no longer runnable. The scheduler does not consider it again until release.

**Where the state lives**

- ==Kernel-internal mutex== — kernel code guarding kernel data. Both the lock byte and the wait queue live in kernel memory; the wait queue can sit inline as a field of the mutex struct.
- ==User-space mutex== — the lock byte lives in user memory. Uncontended acquire is a user-space `TSL` with no syscall. On contention, the user-space library makes a syscall passing the byte's address; the kernel parks the thread on a wait queue keyed by that address.
- The wait queue is always kernel state. The lock's address is the bridge between user memory (where the lock byte lives) and the kernel's wait-queue table.

**Lost wakeup race**

- The `TSL`-failed-then-`sleep` pair is not atomic. Between the two steps the holder may release and call `wakeup` while the queue is empty — the wakeup vanishes; the sleeper sleeps forever.
- The kernel implementation must bundle the queue-and-sleep under its own internal lock so this window does not exist. The canonical DIY failure using bare `sleep`/`wakeup` is in [[semaphores#The Lost Wakeup Problem]].

# Priority Inversion

- A failure mode of [[schedulers#Dynamic Priority|priority scheduling]] when a lock crosses priority levels. Three threads at priorities low (`L`), medium (`M`), high (`H`). `L` and `H` share a lock; `M` is unrelated.

```
1. L acquires the lock and enters its critical section.
2. H becomes runnable, preempts L. H tries to acquire the lock.
3. The lock is held by L. H spins (or blocks) waiting.
4. M becomes runnable. The scheduler prefers M over L.
5. M runs. L never gets the CPU. L never releases the lock.
6. H is stuck behind L, which is stuck behind M.
```

- The high-priority thread waits indirectly on a medium-priority thread that never touches the lock. The medium thread "inverts" the priority order.
- Mars Pathfinder, 1997: a low-priority weather task held a bus lock; a medium-priority comms task starved the lock holder; a high-priority bus task stalled; the watchdog rebooted the lander. Patched from 140 million miles by uploading a priority-inheritance configuration for the lock.

# Priority Inheritance

- The fix: while a thread holds a lock, raise its priority to the highest priority of any thread waiting for that lock. On release, drop back.
- In the inversion above, step 3 promotes `L` to `H`'s priority. `L` immediately preempts `M`, finishes the critical section, releases the lock, drops to its original priority. Then `H` runs.
- Mechanism: the lock structure stores its waiters; the scheduler's priority lookup for a lock holder consults the max waiter priority instead of the holder's nominal priority.
