- A process in the [[os|kernel]] that coordinates the running of user processes.
	- Schedulers do not order the [[processes#Process Queue|process queue]] itself.
	- Schedulers decide the order to run the processes in the ready queue. 
- There are tons of different scheduling algorithms with different goals.

```
USER SPACE
+-------------+                              +-------------+
| Process 1   |                              | Process 2   |
+------+------+                              +------+------+
       |  save (trap to kernel)                     ^  restore to user
=======|============================================|==================
KERNEL |  SPACE                                     |
       v                                            |
+-------------+  switch  +-----------+  switch  +-------------+
| kstack      |--------->| kstack    |--------->| kstack      |
| proc 1      |          | scheduler |          | proc 2      |
+-------------+          +-----------+          +-------------+
```

1. **Save**. The CPU traps into [[os#OS Spaces|kernel mode]] and traps the process. 
2. **Switch to scheduler**. The kernel commits a [[schedulers#Context Switch|context switch]] to the scheduler.
3. **Run scheduler**. Scheduler algorithm then reads the [[processes#Process Control Block|PCBs]] of the processes in queue and context switches to the chosen process.
4. **Restore**. New process should have the same [[cpu#Programmer-visible state|register values]] as when it was suspended. The process is returned to the [[os#OS Spaces|user space]].

# Preemption

- ==Non-Preemptive schedulers== let [[processes]] run until they block on I/O or yield voluntarily.
- ==Preemptive schedulers== interrupts processes based on a timer.

# Round Robin

- A simple, preemptive scheduling algorithm
- Run a process until its quantum is used up, then run the next one in the [[processes#Five State Model|ready queue]].
	-  A ==quantum== is just a fixed amount of time that a process gets to run.

# Dynamic Priority

- Obviously certain processes are larger or more important than others. Thus, we assign a priority value to each.
- $Priority = \frac {1}{f}$, $f$ = fraction of quantum used.
	- Round to the nearest integer.
	- Lower the priority value, higher the priority.
- We create separate process queues for each priority level in the ready queue.

```
+------------+---+---+---+---+
| priority 1 | D | C | B | A |---> highest priority, runs next
+------------+---+---+---+---+
| priority 2 | G | F | E |
+------------+---+---+---+
| priority 3 | J | I | H |
+------------+---+---+---+
```

- A problem: if priority queue 1 remains saturated, processes in other queues will never get a chance to run.

# Lottery Scheduling

- 



# Multiplexing

- There will always be more processes running than processors. 
- The OS splits the physical processor into multiple virtual processors, this is called ==multiplexing==.
- The OS will always allocate itself with its own virtual processor.

# Task State Segment (TSS)


# Context Switch

- Remember that context switches are relatively expensive.
- Consider a scenerio that:
	- Context switch costs 1ms, and our quantum is 4ms.
	- 20% of the time is spent just on context switching
- A solution would be to increase the length of our quantum, but then it will take longer for new processes to run. 

**Variable Quantums**

- Thus, we set custom quantums depending on the type of process.
	- For example, I/O processes should have a shorter quantums to avoid waiting for inputs that may never come.


[[threads]]
