- ==Concurrency== is when multiple units of execution make progress in overlapping time periods.
	- The unit is typically a [[threads|thread]] or a [[processes|process]]. 
	- [[cpu|CPUs]] have multiple [[cpu#Cores|cores]] that sit idle unless given separate work, and the CPU has something else to run during the wait for long processes.
- Concurrency produces two distinct speed gains.

**Latency hiding**

- I/O-bound work spends most of its time blocked on disk, network, or user input.
- While one [[threads|thread]] blocks, the [[schedulers|scheduler]] runs another. The core stays busy instead of stalling and increasing CPU throughput.

# Parallelism 

**Concurrency**

- ==Concurrency== is a property of program structure. The programmer has delegated the computation into in multiple parts that may overlap.

**Parallelism**

- ==Parallelism== is a property of execution. The parts of computation must occur simultaneously.
- A stricter definition of concurrency, and not exactly the same.

# One core, many threads

```
time -->                         
Core 0: [A][B][A][B][A][B]       
```

- Concurrent but not parallel.
- The [[schedulers|scheduler]] time-slices threads onto a single [[cpu#Cores|core]].
- Hides latency but does not increase raw CPU throughput.

# N cores, N threads

```
time -->

Core 0: [A][A][A][A][A][A]
Core 1: [B][B][B][B][B][B]
```

- Concurrent and parallel.
- If more cores exist, the [[os]] can delegate [[threads]] or [[processes]] to them in parallel.
- Exponentially increases CPU throughput.
	- Most, if not all, modern programs leverages multi-core processing.

# Atomicness

- Suppose a variable `count` in [[c]].
- Then,`count++` [[compilers|compiles]] to three [[x86 assembly]] instructions:

```nasm
mov eax [count]   ; read current value from memory into register
add eax 1         ; increment the register
mov [count] eax   ; write result back to memory
```

- Though `count++` appears to be one line, it requires 3 cpu clock cycles.
- ==Atomic Operations== refer to operations that completes in a single cpu [[cpu#The clock|clock cycle]]. 
- Non-atomic operations leads to ==race windows==, a time window where another process dependent on the non-atomic operation [executes]() before the non-atomic operation completes, leading to unpredictable behavior from the dependent operation.

# Race Condition

* [Child processes](processes#Fork) are unlikely to introduce race conditions in the [[memory]].
	* Each process has an independent [[memory#Address Space|address spaces]].
	* The [[compilers|compiler]] has already addressed pre-existing race conditions.
* However, parallel multi-threading almost always cause race conditions.
	* Global variables are shared.
	* The [[compilers|compiler]] cannot address memory race conditions across threads. [[pipelining]] only applies to individual units of compilation in isolation.

- Consider the following example, each thread performs `count++` 10000 times.

```c
#include <stdio.h>
#include <pthread.h>

int count = 0;  

void *increment(void *arg) {
    for (int i = 0; i < 100000; i++) {
        count++;
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, increment, NULL);
    pthread_create(&t2, NULL, increment, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("count = %d\n", count);
    return 0;
}
```

- A programmer might expect the program to output `count = 20000`. 
- However, in reality, the result is unpredictable and most likely lower.
- Consider the operation `count++` across two cores and [[cpu#The clock|clock cycles]] $n$.

```
|        |          | n=0             | n=1       | n=2             |
| ------ | -------- | --------------- | --------- | --------------- |
| core 1 | thread 1 | mov eax [count] | add eax 1 | mov [count] eax |
| core 1 | thread 2 | mov eax [count] | add eax 1 | mov [count] eax |
```

- After $n=2$ in the example above, `count = 1` despite threads `t1` and `t2` performing `count++` twice.
- This is because the two [[threads]] share a global `count` variable. One thread can read `count` before the other has finished the incrementation. Resulting in both threads performing identical operations, and writing identical data back into memory.
- This is a [[pipelining#Hazards|write-after-write]] hazard. 

# Critical Section

- A segment of code that accesses a ==shared resource==.
- A shared resource is a variable, file, or device that cannot be accessed concurrently.
- In our example:

```c
// Critical Section
count++;

// Shared Resource
int count = 0;
```

**Solution**

- Every solution to the critical section problem will follow the following three properties.

 **Mutual Exclusion**

- The fix of any race condition is to allow only 1 visitor in a critical section at a time.
- In our example, the fix would be to allow only one thread to execute `count++` at a time. Effectively addressing the [[pipelining#Hazards|write-after-write]] error.

**Liveness**

- If multiple threads request entry simultaneously, only one can be allowed to proceed.
- The decision must depend only on threads currently competing, threads outside the critical section should not block entry.

**Bounded waiting**

- A thread that has requested entry must eventually be allowed in. No thread waits forever while others repeatedly enter ahead of it.