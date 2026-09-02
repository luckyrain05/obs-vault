- A pathology of [[locks|lock]]-based and [[semaphores|semaphore]]-based synchronization. When a set of threads each waits on a resource held by another in the same set, no one progresses.
- ==A set of processes is deadlocked if each process in the set is waiting for an event that only another process in the set can cause.==
- The note covers the formal conditions, how to model them as a graph, and the four families of strategies for handling deadlock.

# Resource Types

**Non-preemptible**

- Once granted, cannot be taken away without cooperation from the holder.
- Examples: a [[locks|mutex]], a printer mid-job, a CD-burner. Forcing the holder to release leaves the resource in a corrupt state.
- Deadlock is a problem only with non-preemptible resources.

**Preemptible**

- Can be taken from the holder without harm.
- Preemptible resources do not deadlock — the system simply reclaims them.

# The Four Conditions (Coffman)

- All four must hold simultaneously for a deadlock to be possible. Negating any one prevents it.

1. ==Mutual exclusion== — each resource is held by exactly one process or is free.
2. ==Hold and wait== — a process holding resources can request more.
3. ==No preemption== — a held resource cannot be forcibly taken; only the holder releases it.
4. ==Circular wait== — there is a cycle of two or more processes, each waiting on a resource held by the next.

# Resource Allocation Graph

- A directed graph that models who holds what and who wants what.
- Two node types: ==process== (circle) and ==resource== (square).
- Two edge types:
	- Resource → process: the resource is currently held by the process.
	- Process → resource: the process is blocked waiting to acquire the resource.

```
         +---+         +---+
         | R | ----->  ( A )
         +---+         +---+
                         |
                         v
                       +---+
                       | S |
                       +---+
                         |
                         v
                       +---+
                       ( B )
                       +---+
                         |
                         v
                       +---+
                       | R |   <-- cycle closes back to R
                       +---+
```

- Process A holds R, wants S. Process B holds S, wants R. Edges form a cycle A → S → B → R → A. Deadlock.

# Detection

- A deadlock exists if and only if the resource allocation graph contains a cycle (when each resource has one instance).
- Detection algorithm: depth-first search from each node, looking for a back edge.

```
    Cycle present                  No cycle
   --------------                ---------------
   (A)----+                      (A)----+
    ^     |                       ^     |
    |     v                       |     v
   [R]   [S]                     [R]   [S]
    ^     |                              ^
    |     v                              |
    +----(B)                            (B)
```

- Detection is cheap; the work is what to do once a cycle is found.

# Prevention

- Negate one of the four Coffman conditions in the system's design.

**Break mutual exclusion**

- Make resources sharable. Most resources cannot be made sharable without losing their meaning (a printer's output would interleave). Limited applicability.

**Break hold-and-wait**

- Force every process to acquire all the resources it will ever need at once, before starting work. If it cannot get them all, it gets none and tries again later.
- Inefficient: resources sit idle while reserved.

**Break no-preemption**

- Allow the OS to forcibly revoke a held resource. Works for [[virtual memory#Page Hits and Page Faults|memory pages]] (swap to disk) and CPU time slices. Does not work for mutexes mid-update.

**Break circular wait**

- Order all resources globally. Each process must acquire resources in increasing order of that ordering.
- A cycle would require some process to acquire a lower-numbered resource while holding a higher-numbered one — forbidden by the rule. No cycle is possible.
- Most practical of the four. Linux kernel locks document an acquisition order; lockdep reports violations.

# Avoidance

- Distinct from prevention: at every allocation request, the system simulates whether granting the request can lead to a state where deadlock becomes inevitable. If yes, deny the request even if the resource is free.
- Requires advance knowledge of every process's maximum resource demand. Banker's algorithm is the textbook implementation: a state is ==safe== if there exists some scheduling of remaining requests in which all processes complete.
- Used rarely in practice — the maximum-demand assumption is usually unrealistic.

# Detect and Recover

- Skip prevention and avoidance. Run the system normally; periodically run the cycle-detection algorithm. On a cycle, recover by:
	- Killing one process in the cycle (loses its work).
	- Rolling back a process to a checkpoint and restarting it.
	- Forcibly preempting a resource (corrupts state — only safe for some resource types).

- The "do nothing" strategy is the limit case: rely on the deadlock being rare enough that crashing the system or rebooting is acceptable. UNIX historically took this approach for kernel deadlocks.

# Dining Philosophers

- Five philosophers at a round table. Five forks between them. To eat, a philosopher needs the fork on their left and the fork on their right.

```
            P0
         /      \
       F4        F0
       |          |
       P4        P1
       |          |
       F3        F1
         \      /
            P2 -- F2
```

**Naive solution**

```c
void philosopher(int i) {
    while (1) {
        think();
        take_fork(i);              // left
        take_fork((i + 1) % N);    // right
        eat();
        put_fork(i);
        put_fork((i + 1) % N);
    }
}
```

- Failure: every philosopher picks up their left fork at the same instant. Each holds one fork and waits on the right one held by their neighbor. All four Coffman conditions hold. The graph has a five-cycle. Deadlock.

**Single mutex around all forks**

- Wrap fork acquisition in one global mutex: only one philosopher eats at a time.
- Correct but inefficient — `N - 1` philosophers idle even when non-adjacent pairs could eat in parallel.

**Random backoff**

- After picking up the left fork, if the right is unavailable, drop the left and wait a random interval. Probabilistically avoids the synchronized-deadlock pattern.
- Not deterministic. Pathological schedules can still deadlock; for hard-real-time systems this is unacceptable.

**State array with per-philosopher semaphore**

- Each philosopher has a state in `{THINKING, HUNGRY, EATING}` and a personal semaphore `s[i]`. A single mutex protects the state array.

```c
#define LEFT  ((i + N - 1) % N)
#define RIGHT ((i + 1) % N)
int state[N];
semaphore mutex = 1;
semaphore s[N];

void take_forks(int i) {
    down(&mutex);
    state[i] = HUNGRY;
    test(i);                  // try to acquire two forks
    up(&mutex);
    down(&s[i]);              // block here if test() didn't grant
}

void put_forks(int i) {
    down(&mutex);
    state[i] = THINKING;
    test(LEFT);               // can left neighbour eat now?
    test(RIGHT);              // can right neighbour eat now?
    up(&mutex);
}

void test(int i) {
    if (state[i] == HUNGRY
        && state[LEFT]  != EATING
        && state[RIGHT] != EATING) {
        state[i] = EATING;
        up(&s[i]);            // grant both forks
    }
}
```

- A philosopher's transition to `EATING` happens only when both neighbours are not eating, under the global mutex. Two non-adjacent philosophers can eat in parallel. No cycle is possible: a philosopher only proceeds when neighbours are confirmed not to hold their shared forks.
