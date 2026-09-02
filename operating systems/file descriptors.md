# I/O and File Descriptors

**File Descriptor**: integer representing "kernel managed" object that can be read or written.
- Includes files, dirs, devices, pipes. Pipes will be covered.
- Every process inherits three default file descriptors:
	- `stdin`: 0
	- `stdout`: 1
	- `stderr`: 2
- xv6 has the `open()` [[system calls|system call]]. It returns a FD given the filename and path.
- Once fd is obtained, it can be used with other [[api|APIs]]:
	- `read(int fd, void *buf, int n)`
	- `write(int fd, void *buf, int n)`
		- `*buf` is the data, `n` is the number of bytes.

# Redirection

- `stdin` and `stdout` can be redirected from file to file.
	- Input with `<`
	- Output with`>`
	- Search for the word `word` in the file `README` using the process `grep`,  save the results to a file `found.txt`.
		- `grep word README`
		- `grep word < README > found.txt`
	- `README` after `<` takes place of `stdin`, `found.txt` becomes `stdout` after `>` .

# Pipes

- `pipe()` is called by the shell with `|`.
- Suppose the command line `a | b`, process `a`'s `stdout` becomes process`b`'s `stdin`, so forth.

# Kernel Data Structures

- An FD is a small integer because the kernel uses it as an array index. Three layers of indirection sit between the FD and the on-disk file.

- Per-process FD table: array of pointers, one per FD. Indexed by the integer the user holds. Each entry points to an entry in the next layer. Lives in the [[processes|process]]'s PCB. Each process has its own table; FD 3 in process A and FD 3 in process B are unrelated.

- System-wide open file table: one entry per `open()` call across the whole system. Stores the current file offset, the open flags (read/write/append), and a refcount of how many FDs point at this entry. The offset lives here so two independent `open()`s on the same file get independent positions, but two FDs sharing one open-file-table entry share a position.

- Inode: per-file metadata and block pointers ([[file systems#Inode Block Pointers]]). Refcount-tracked separately from the open-file table: many open-file-table entries can point at one inode, and the inode itself has a [[file systems#Hard and Symbolic Links|hard-link refcount]] counting directory entries.

```
  Process A                Kernel global              On-disk
                          (open file table)
  +-------+
  | FD 0  |---+
  +-------+   \           +------------------+         +---------+
  | FD 1  |---+---------->| offset=512       |         | inode 7 |
  +-------+   /           | flags=O_RDONLY   |-------->| size    |
  | FD 2  |--+            | refcount=2       |         | blocks  |
  +-------+               +------------------+         +---------+
  | FD 3  |-------------->| offset=4096      |
  +-------+               | flags=O_WRONLY   |
                          | refcount=1       |
  Process B               +------------------+
  +-------+   /
  | FD 0  |--+
  +-------+
```

# dup, fork, exec

- The three operations that mutate FD relationships, each in a distinct way.

**dup(fd)**

- Allocate a new FD slot in the same process; point it at the same open-file-table entry. Increment the refcount on that entry.
- Result: two FDs in the same process share offset and flags. A `read` on one advances the position seen by both.
- Used to implement shell redirection: the shell `dup()`s a target FD onto FD 0/1/2 before `exec()`.

**[[processes#Fork|fork()]]**

- The child gets a copy of the parent's FD table. Each entry points at the *same* open-file-table entry as the parent's. Refcount on each entry is incremented.
- Result: parent and child share offsets and flags, just like `dup`. A `read` in either advances the position for both.

**exec()**

- The FD table survives `exec()` by default. The new program inherits all open FDs at their current positions.
- The `O_CLOEXEC` flag (close-on-exec) on a specific FD changes this — that FD is closed automatically when `exec` succeeds. Used for FDs that the new program should not see (privileged sockets, tempfiles).
