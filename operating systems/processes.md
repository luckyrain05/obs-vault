- A ==program== is just instructions on disk; a ==process== is the correct unit for a program's said instructions loaded and executed by the [[os]].
- Processes containers with a [[virtual memory#Page Tables|page table]] and [[cpu#Programmer-visible state|register values]] ready to execute instructions from any program.
	- Conceptually, it is the tooling that the [[os]] provides for it to execute programs.
	- The shell is a permanently running process used to run any program on demand.

**Process Spaces**

-  Every process is allocated two [[memory#Stacks|stacks]], the ==user-stack== and ==kernel-stack==.
	- While executing instructions, the [[os#OS Spaces|kernel]] stack remains empty and the [[os#OS Spaces|user]] stack is in use.
	- Until a [[system calls|system call]] traps the process to the kernel. The kernel then executes on the kernel stack of the thread.
	- User stack and kernel stack are kept separate.

# [[Threads]]

  - A ==thread== is an unit of execution within a process that executes the processes instructions.
  - Every process has at least one thread that starts the `main()` of the program.
  - Like how process is an instance of a program, a thread is an instance of a process.

# Process Control Block

- The ==PCB== is structured metadata for the os to store and remember the process.
- Every process has exactly one PCB. The os creates it on process creation and destroys it on exit.
- Implemented as a struct in [[c]].

**Process ID**

- Unique identifier for the process, also called ==PID==.
- It is a specific data type `pid_t` in [[c]].

**Process State** 

- Which state in the state model the process is currently in.
- Will elaborate below.

**Program Counter**

- Address of the next instruction to execute when resumed.

**CPU Registers**

- The register values last written to the [[cpu]].

**Memory Management Info**

- Page tables, base/limit registers, etc. 
- Everything the OS needs to reconstruct the process's [[memory#Address Space|address space]].

**I/O Status** 

- Open files, allocated devices.

**Scheduling Info**

- Consisting of priority value, [[schedulers#Round Robin|quantum]], queue pointers. 
- The [[schedulers|scheduler]] reads this to make dispatch decisions.

# Process Table

- The ==process table== is a kernel data structure that holds every active PCB in the system.
- Implemented with different data structures depending on the os.
- The maximum number of [[concurrency|concurrent]] processes is bounded by the size of this table.

# Process Queue

- ==Process queue== is a set of only `ready` or `RUNNABLE` processes in the process table.
- [[Schedulers]] read this to decide the next process to run.
- Implemented with different data structures depending on the os.

```
+---+---+---+---+---+
| A | B | C | D | E | -----> CPU
+---+---+---+---+---+
```

# Two State Model

- Every process needs a means of termination, obviously.
- Thus we can derive two states of processes, running and not running (paused).

```

			+---+---+---+---+  dispatch   +-------+
enter ---->	| E | D | C | B |---------->  |  CPU  |----> exit
			+---+---+---+---+             +-------+
		      queue                           |
				^                             |
		        +-----------------------------+
				          pause
```

- Uses a single process queue.
- Paused programs are sent to the back again.

# Five State Model

- A paused process waiting on I/O shouldn't compete with processes ready to run.
- We split "not running" into more granular states to solve this problem.

1. **New**
	- Process has been created but not yet admitted to the ready queue.
2. **Ready** or **RUNNABLE**
	- Process is in the ready queue, loaded in memory and waiting to be dispatched.
3. **Running**
	- Process is currently executing on the CPU. Only one process per CPU can be in this state.
4. **Blocked/Sleeping**
	- Process is in the blocked queue, waiting on an event. Cannot run even if the CPU is free.
5. **Exit**
	- Process has terminated. OS cleans up its resources.

- Instead of one queue, we now use two: a ==ready queue== and a ==blocked queue==.
	- The ready queue holds processes that can run immediately.
	- The blocked queue holds processes waiting on an event.

```
             +------------------------------------------------+
             |                    timeout                     |
             v               dispatch                        |
+-------+  admit  +-------+ ---------> +---------+  release  +------+
|  New  |-------->| Ready |            | Running |---------->| Exit |
+-------+         +-------+ <--------- +---------+           +------+
                      ^                    |
                      |    event           |  event
                      |    complete        |  wait
                      |                    v
                      |             +---------+
                      +-------------| Blocked |
                                    +---------+
```

- The scheduler only pulls from the ready queue.
- The blocked queue pushes into the ready queue when unblocked (event completed).
- ==This is the model we will use.==

# [[System Calls]]

- There are four main [[system calls]] in [[c]] used to manage processes.

**Exit**

```c
#include <stdlib.h>

void exit(int status);        // standard, runs atexit() handlers, 
void _exit(int status);       // raw syscall, bypasses all cleanup
```

**Fork**

```c
#include <unistd.h>

pid_t fork(void);
```

**Wait**

```c
#include <sys/wait.h>

pid_t wait(int *wstatus);
```

**Exec**

```c
#include <unistd.h> 
int execve(
	const char *pathname, 
	char *const argv[], 
	char *const envp[] );
```

1. `void exit(int status);`
2. `pid_t fork(void);`
3. `pid_t wait(int *wstatus);`
4. `int execve(const char *pathname, char *const argv[], char *const envp[]);`

# Exit

- `void exit(int status)` terminates the calling process.
	- Returns nothing.
	- The field`status` is the exit code. `1` means exited with errors, `0` means no errors.
	- Which ever process runs into `exit()` will kill itself, regardless of generation.

**Steps**

1. Closes all open file descriptors.
2. Releases the process's [[virtual memory#Page Tables|page table]] and user memory.
3. Reparents any children to [[boot#init|init]] so they are not orphaned.
4. Wakes up the parent if it is blocked in `wait()`.
5. Sets the process state to zombie. The PCB remains until the parent reaps it.

- The process cannot free its own kernel stack or PCB. The parent's `wait()` call handles the final cleanup.

# Fork

- `fork(void)` makes an exact copy of the current process as it's child process.
	- Returns data type `pid_t`. 0 for child, PID of child for parent.
	- Suppose the line `pid_t i = fork()`. The kernel will populate parent's `i` with the PID of the child, and `0` in the child's `i` to indicate that it is the child.

- The child process continues right after the `fork()` call. 
- Children can have more children.
- The child process is queued like every other process. 

**Steps**

1. Enters [[os#OS Spaces|kernel mode]]. Duplicates the current running process in its entirety.
2. Set the return value for the system call for both the original and duplicate.
3. Puts both processes in the [[schedulers|scheduler queue]].
4. Mark the children RUNNABLE.

```c
pid = fork();
printf("both parent and child print this\n");

# only the child's pid is 0
if (pid == 0) {
    printf("i am the child\n"); 
}
else { 
	prinf("i am the parent\n");
}
```

- Suppose the program below. How many times does it print `foo`?

```c
#include <stdio.h>
#include <unistd.h>

int main(void) {
	int i = 0;
	for (i = 0; i < 4; i++) {
		fork();
		printf("foo\n");
	}
	return 0;
}
```

- The answer is 30 times. 
- Remember, the value of `i` in the forloop is copied to the children as well. It keeps splitting until `i = 3`. In which case all programs will finish.

```
i = 0 foo * 2


i = 1 foo * 4


i = 2 foo * 8


i = 3 foo * 16
```

- How many times foo is printed at each `i` value. They total 30.

# Wait

- `pid_t wait(int *status)` blocks the calling process until the first children exits.

```c
int status;
pid_t child = wait(&status);
```

- Returns the PID of the exited children, -1 if the calling process does not have children.
- Kernel will write the exit status to the memory address in the parameter.
- Calling `wait(NULL)` disregards the status. 
- The typical `fork()` + `wait()` pattern:

```c
pid = fork();
if (pid == 0) {
    // child does work
    exit(0);
}
// parent waits for child to finish
wait(&status);
```

- Without `wait()`, terminated children accumulate as ==zombies==.

# Zombies

- A ==zombie== is a child process who has exited, but its parents did not call `wait()`.
- The moment any child exits, the process table will mark it as a zombie.
- Once the parent process executes `wait()`, the [[os#OS Spaces|os]] reaps the zombie and removes its PCB from the process table.

**Innit**

- If the parent exits without ever calling `wait()`, [[boot#init|init]] will adopt the newly orphaned process. 
- Zombies are harmless individually but problematic in bulk.

# Exec

- `exec(char *path, char *argv[])` replaces the program that the calling process is running with another one. Completely nukes the calling process.
	- Returns nothing on success, -1 on failure. 
- Consider the code below:

```c
pid = fork();
if (pid == 0) {
    exec("/bin/ls", args); 
}
```

- The child process no longer executes the program that it came from.
- Instead, it runs the user program `ls`.

**Steps**

1. **Set up user [[virtual memory#Page Tables|page table]].**
	- Enters [[os#OS Spaces|kernel mode]]. Nukes the current process's page table since we will not be running whatever process it currently is running anymore.

2. **Load new program into page table**
	- Kernel reads the executable of the new program and loads that in to the page table we just reset. 

3. **Set up stack and arguments.**
	- It allocates a page for the user stack of the process at the top of the [[virtual memory|virtual address space]].
	- Then pushes `argv` strings onto it, followed by the `argv[]` pointer array, then `argc`. 
	- This mimics what a [[c]] runtime would do, so when `main(int argc, char* argv[])` starts executing, the arguments are exactly where the calling convention expects them.

4. **Jump to entry point.**
	- The process returns to [[os#OS Spaces|user mode]], it starts executing the new program as if it was freshly launched.

- `exec()` doesn't create a new process. The PCB remains the same. 
- It only replaces what the process is running. That's why the Unix model is `fork()` then `exec()`, fork copies the process, exec replaces the one that is currently running.
