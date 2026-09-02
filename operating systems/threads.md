- Sometimes, we need parts of a [[processes|process]] to run [[concurrency|concurrently]].
- Thus we invent ==threads==, which are stages of executions within a process.
	- Similar to how programs can run concurrently with multiple processes, threads are just one more level down from that.
	- However, [[schedulers#Context Switch|context switches]] are much faster since threads are smaller.

- A process with more than one thread is ==multi-threaded==. Threads are created by the programmer using [[threads#pthread|thread libraries]].
- Multi-threading always gives [[concurrency]]. Whether it also gives [[concurrency|parallelism]] is a separate question, decided by the user-to-kernel mapping model and the number of [[cpu#Cores|cores]] available.

# Structure

- Every thread is allocated their own [[memory#Stacks|stack]].
- Threads share the [[memory#Heaps|heap]], [[compilers#Data|data]], and [[compilers#BSS|bss]], of their parent processes.
- Every [[c]] program has one process has at least one thread that runs `main()`.

# User vs Kernel Threads

**User Threads**

- ==User threads== are managed entirely in [[os#OS Spaces|user space]] by a thread library. The [[system calls|kernel]] is not aware of them. Thread creation, scheduling, and destruction are handled by the library.
- Fast to create and switch between because no trap to [[os#OS Spaces|kernel mode]] is needed.

- We obviously wouldn't be able to make [[system calls]] this way, so we ned ==kernel threads== to map the user threads to.

**Kernel Threads**

- Kernel threads are managed directly by the [[system calls|kernel]]. The OS creates, schedules, and destroys them.
- Each kernel thread can be independently [[schedulers|scheduled]]. If one blocks on I/O, the kernel can run another from the same [[processes|process]].
- Creation and [[schedulers#Context Switch|context switches]] are slower than user threads because each operation requires a trap to [[os#OS Spaces|kernel mode]].

- There are many models that map user threads to kernel threads.

# Parallelism

- A thread's execution flows through three layers, each with its own scheduler.

```
+-----------------+
|  user thread    |
+-----------------+
        |
        |   thread library scheduler  (only matters in M:1 and M:M)
        v
+-----------------+
|  kernel thread  |
+-----------------+
        |
        |   kernel scheduler
        v
+-----------------+
|    CPU core     |
+-----------------+
```

- [[concurrency|Concurrency]] arises the moment a process has more than one user thread, regardless of mapping. The threads exist and overlap in logical time.
- [[concurrency|Parallelism]] requires two things at once: the kernel must see more than one schedulable entity for the process, AND there must be more than one [[cpu#Cores|core]]. The kernel [[schedulers|scheduler]] then dispatches each kernel thread onto its own core simultaneously.
- The narrowest layer caps parallelism. If the user-to-kernel mapping funnels every user thread through one kernel thread, that single kernel thread is the cap regardless of core count.

# Many to One

- Many user threads map to a single kernel thread.
- The thread library runs its own scheduler in user space, time-slicing user threads onto the one kernel thread. The kernel knows nothing about the individual user threads.
- Multi-threaded but not parallel. Even on an N-core machine, only one user thread runs at any instant because the kernel sees one schedulable entity.
- If any user thread blocks on a [[system calls|system call]], the entire process is blocked. The kernel cannot pick another user thread because it does not see them; the library cannot pick another either because the one kernel thread is stuck in the kernel.

```
  +------+  +------+  +------+  +------+
  |  UT  |  |  UT  |  |  UT  |  |  UT  |
  +--+---+  +--+---+  +---+--+  +--+---+
     |         |           |        |
     +---------+-----+-----+--------+
			         |
  ===================|=================== Kernel
                     |
                     v
                 +------+
			     |  KT  |
                 +------+
```

# One to One

- Each user thread maps to its own kernel thread. The thread library has no scheduler of its own; every scheduling decision is the kernel's.
- True parallelism up to the number of [[cpu#Cores|cores]]. The kernel scheduler can dispatch every kernel thread on its own core simultaneously.
- A blocking [[system calls|system call]] in one thread does not block the others.
- Overhead is higher. Every thread creation requires a kernel thread creation, which is a [[system calls|system call]]. Most implementations cap the number of threads.
- Linux and Windows use this model.

```
  +------+  +------+  +------+  +------+
  |  UT  |  |  UT  |  |  UT  |  |  UT  |
  +--+---+  +--+---+  +---+--+  +--+---+
     |         |          |        |
  ===|=========|==========|========|==== Kernel
     |         |          |        |
     |         |          |        |
     v         v          v        v
  +------+  +------+  +------+  +------+
  |  KT  |  |  KT  |  |  KT  |  |  KT  |
  +------+  +------+  +------+  +------+
```

# Many to Many

- Many user threads map to an equal or smaller number of kernel threads.
- The thread library multiplexes user threads onto the available kernel threads.
- Blocking [[system calls|system call]] in one user thread does not block the others because the library can remap them to a free kernel thread.
- True parallelism up to the number of kernel threads.

```
  +------+  +------+  +------+  +------+
  |  UT  |  |  UT  |  |  UT  |  |  UT  |
  +--+---+  +---+--+  +--+---+  +---+--+
     |          |         |          |
     +----+-----+         +----+-----+
          |                    |
  ========|====================|======== Kernel
          |                    |
	 +----+----+          +----+----+          
	 |         |          |         | 
	 v         v          v         v      
  +------+  +------+   +------+  +------+
  |  KT  |  |  KT  |   |  KT  |  |  KT  | 
  +------+  +------+   +------+  +------+ 
```

# Two Levels

- A variation of many to many that also allows a user thread to be permanently bound to a dedicated kernel thread.
- Bound threads get one-to-one treatment for latency-sensitive work.
- Unbound threads share kernel threads via the many-to-many model.

```
  +------+  +------+  +------+  +------+
  |  UT  |  |  UT  |  |  UT  |  |  UT  |
  +--+---+  +---+--+  +--+---+  +--+---+
     |          |         |         |
     +----+-----+         |         |  
          |               |         |    
  ========|===============|=========|=== Kernel
          |               |         |
          v               v         v
       +------+        +------+  +------+
       |  KT  |        |  KT  |  |  KT  |
       +------+        +------+  +------+
```

# Thread Control Block (TCB)

- Just like [[processes#Process Control Block|PCBs]], a TCB is structured metadata for the OS to store threads.
- Every thread has exactly one TCB. Created on thread creation, destroyed on thread exit.

**Thread ID**

- Unique identifier for the thread, also called ==TID==.

**Thread State**

- Which of the five states the thread is currently in (same model as processes).

**Program Counter**

- Address of the next instruction to execute when the thread is resumed.

**CPU Registers**

- General-purpose [[cpu#Programmer-visible state|registers]], flags. Saved on context switch, restored on dispatch.

**Stack Pointer**

- Points to the thread's own [[memory#Stacks|stack]]. Each thread has a private stack; the stack pointer is what separates one thread's execution from another.

**Pointer to PCB**

- Every TCB belongs to exactly one [[processes#Process Control Block|PCB]]. The OS uses this to find the owning process's address space and resources.

# Thread Pool

- Creating a new thread for every request is expensive. A ==thread pool== pre-creates a fixed number of threads at startup.
- Incoming tasks are placed in a queue. Idle threads in the pool pick up tasks from the queue.
- Bounds resource usage. The number of active threads is capped by the pool size, preventing the system from being overwhelmed.
- Reusing existing threads avoids the overhead of repeated creation and destruction.

# pthread

- ==pthread== is a [[c]] library for implementing threads.

**Creation**

```c
int pthread_create(	pthread_t *thread, 
					const pthread_attr_t *attr,
					void *(*start_routine)(void*), 
					void *arg
					);
```

**Joining**

```c
int pthread_join(pthread_t thread, void **value_ptr);
```

**Exit**

```c
void pthread_exit(void *value_ptr);
```

