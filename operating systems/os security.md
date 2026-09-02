- The OS access-control model: who is allowed to do what to which kernel-managed object. Enforced at every system call by the kernel, which sits behind the [[os#OS Spaces|privilege boundary]] user code cannot bypass.
- Two things to specify: a ==principal== (the actor making a request) and a ==right== (the operation being requested on a specific ==object==). The kernel checks the principal against the policy attached to the object before allowing the right.

# Principals and Objects

**Principal**

- The identity an action is attributed to. On UNIX: a numeric ==UID== (user ID) plus a list of ==GIDs== (group IDs). Each [[processes|process]] inherits these from its parent.
- The kernel sees only numbers. Mapping UIDs to usernames is a userspace convention (`/etc/passwd`).
- UID 0 is ==root==: the kernel skips most permission checks for processes running as UID 0.

**Object**

- Anything the kernel arbitrates access to. [[file systems|Files]] (regular, device, pipe, socket), processes (sending signals, ptrace), shared memory segments, semaphores.
- Each object stores its policy. For files: an inode field with permission bits; for sockets: a file descriptor entry; for processes: the kernel's PCB.

# UNIX Permission Bits

- Every file's [[file systems#Inode Block Pointers|inode]] stores nine permission bits, organized as three rights (read, write, execute) for three principals (the owning user, the owning group, everyone else).

```
  rwx rwx rwx
  --- --- ---
   |   |   +--- other
   |   +------- group
   +----------- owner

  e.g. rwxr-x---  =  owner: read+write+execute
                     group: read+execute
                     other: nothing
```

- On every file access, the kernel:
	1. If the process's UID matches the file's owner UID, check the owner bits.
	2. Else if any of the process's GIDs match the file's group GID, check the group bits.
	3. Else check the other bits.

- Only the first matching set is consulted. A user who is the owner *and* in the group is judged only by the owner bits — even if the group has wider access.

**setuid and setgid**

- Two extra bits in the inode's permission field. When set on an executable, the resulting process runs with the *file's* owner/group, not the invoking user's.
- Used for narrowly-scoped privilege escalation: `passwd` is owned by root with setuid set, so any user who runs it briefly gains root rights to edit `/etc/shadow`. The program is responsible for limiting what it does with the elevated rights.
- Powerful and easy to misuse — a setuid-root binary with a buffer overflow gives an attacker root.

# The Access Matrix

- Conceptually: a giant matrix where rows are principals, columns are objects, cells contain rights.

```
            file1   file2   socket3   process7
   alice    rw-     r--     -         signal
   bob      r--     rwx     rw        -
   root     rwx     rwx     rw        signal
```

- Two ways to store the matrix; each is a transposition of the other:

**Access Control List** (column-store)

- Each *object* stores a list of (principal, rights) pairs. To check an access, look up the object, scan its ACL for the principal.
- UNIX permission bits are a compressed ACL — they encode rights for three principals (owner, group, other) in nine bits. Full ACLs (e.g. POSIX ACLs, NTFS ACLs) allow arbitrarily many principal-rights entries per object.

**Capability** (row-store)

- Each *principal* holds a list of (object, rights) tokens. To access an object, the principal presents the token; the kernel honors the rights named in the token.
- ACLs make "who can access X?" easy and "what can principal Y access?" expensive. Capabilities flip the trade-off.

# Cryptographic Capabilities

- The kernel issues each capability as a token computed by a [[cryptography#Hash Functions|hash function]]:

```
  Token = f(ObjectId + Rights, Secret)
```

- `Secret` is a kernel-only key. The user sees `(ObjectId, Rights, Token)` and cannot recompute `Token` for a different `ObjectId` or `Rights` because they don't know `Secret`.
- On access, the user presents the triple. The kernel recomputes $f$ using the same `Secret`; if the result matches `Token`, the request was not tampered with.
- The capability can live anywhere — in the user's memory, on disk, on a remote machine. The cryptographic check makes forgery infeasible. Used by Kerberos (it calls them ==tickets==) for distributed authentication.

# Enforcement

- The kernel checks permissions at every relevant system call, never before. User code cannot bypass the check because:
	- The check happens at ring 0; user code runs at ring 3.
	- The data structures storing the policy live in kernel memory, mapped supervisor-only in the [[virtual memory#Memory Protection|page table]].
	- The transition from ring 3 to ring 0 only happens via [[software interrupt|trap]] entry points the kernel chose — there is no way to run kernel code that skips the check.
- This is why the OS owns access control in the first place. A library check in user code can be patched, bypassed, or skipped; a kernel check sits behind a hardware-enforced privilege boundary.
