- A file system is an abstraction layer over raw [[memory]] to store and interact with data, provided by the [[os]].
- Like most data interaction strategies, the [[os]] also divide the [[memory#Address Space|address space]] of any storage device into blocks.
	- Typically 512 bytes, or 4KB.
	- The file system's entire purpose is to abstract fragmented blocks in the storage as cohesive objects that is intuitive to the user.
- The file system is handled entirely by the [[os#OS Spaces|kernel]], user space does not see the raw storage blocks.

# Files

- A ==file== is simply defined as a named collection of bytes. It is a basic unit of information.
- Conventionally, file names consist of the name and an extension that identifies the file type, separated by a `.`.
	- However, this is almost never enforced.
	- Some files consist of information in the beginning as the identifier instead.

# Directories

- A ==directory== is a mapping of a name to a collection of files. Conceptually just a folder.
	- Unix and Linux implements directories as simply another file that includes the location of every file in the directory.
	- Windows do not share this philosophy.
- Directories can nest other directories.
	- A ==file path== is a string that identifies the file in the hierarchy of directories.
	- `~/dir1/dir2/dir3/file.txt`

# Block Allocation Strategies

- Files larger than a block obviously must be stored in multiple blocks. 

# Contiguous Allocation

- Literally write the file to sequential blocks in in the address space.
	- Unbeatable reading speeds for storage devices that must manually seek out a physical block location, since they are right next to each other.
- However, as files are created and destroyed, the [[memory#Address Space|address space]] of the storage device becomes ==fragmented==, or the available space becomes patchy and spotty.
	- Overtime, it would be impossible to find a continuous region of unallocated address space, especially for large files.
	- Thus, this strategy cannot be enforced for storage devices that constantly modifies its data.  

# [[linked lists|Linked List]] Allocation

- We use a linked list to link the blocks together. Same downsides.
	- Access to any block is `O(1)` TC.
	- Each block loses a few bytes to the pointer.

```
[ data | next → ] → [ data | next → ] → [ data | NULL ]
```

# FAT

- FAT allocation groups blocks into ==clusters==.
	- A cluster might be 4, 8, 32, or more sectors depending on the FAT variant used.
	- Files are allocated in whole clusters. The remainder is wasted if the file is smaller.
-  The ==file allocation table== is an [[arrays|array]] of cluster addresses.
	- `FAT[x]` will hold the pointer to the next cluster after $x$, etc.
	- This way we separate the pointer from the data blocks.

```
FAT:  [ 9 ][ 0 ][ 0 ][ 0 ][ 12 ][ 0 ][ EOF ] ...
Data: [ .......... ] [ .......... ] [ .......... ]
```

- Depending on storage size, FAT will use different [[memory#Memory Addresses|address widths]].

# **Inodes**

- Each file has an ==inode== (index node), a small fixed-size on-disk structure storing the file's metadata and a list of its block numbers. The directory entry holds the inode number.
- Memory cost grows with the number of *open* files, not total files or disk size — only inodes for currently-open files need to be in RAM.
- Used by ext2/3/4, UFS, xv6.

# Inode Block Pointers

- An inode has a fixed number of slots, but file sizes are unbounded. The trick is multi-level indirection.

```
  Inode
  +-----------------------+
  | metadata (size, perm, |
  | timestamps, owner)    |
  +-----------------------+
  | direct[0]      ----------> data block
  | direct[1]      ----------> data block
  |    ...         (12 entries on ext2)
  | direct[11]     ----------> data block
  +-----------------------+
  | indirect       ----------> [block of pointers] -> data blocks
  +-----------------------+
  | double indirect---------> [block of pointers] -> [block of pointers] -> data
  +-----------------------+
  | triple indirect---------> [...] -> [...] -> [...] -> data
  +-----------------------+
```

- Direct entries reach the first ~12 × 4KB = 48KB without indirection.
- An indirect block (say 1024 pointers in 4KB) reaches another 4MB through one extra disk read.
- Double indirect adds $1024^2$ blocks (4GB); triple indirect $1024^3$ blocks (4TB).
- Small files cost only their inode and a few direct blocks; large files pay one extra disk read per indirection level. Common case is fast.

# Hard and Symbolic Links

- Two ways to give one file multiple names.

**Hard link**

- A second directory entry pointing to the same inode. Both names are equally "real" — neither is the original. Deleting one decrements the inode's reference count; only when the count reaches zero is the inode (and its data blocks) freed.
- Cannot cross file systems (the target inode number is meaningful only within one FS).
- Cannot point to a directory (would create cycles in the tree, breaking traversal).

**Symbolic link** (symlink)

- A small file whose contents are a path string. When the OS encounters a symlink during path resolution, it substitutes the contents and continues resolving from there.
- Can cross file systems and link to directories. The cost: an extra path resolution per symlink hop, and the link can dangle if the target moves.
- Deleting the target leaves the symlink intact but broken; deleting the symlink leaves the target untouched.

# Free Space Management

- The FS must know which blocks are free. Two representations:

**Free list**

- Linked list of free blocks, each containing pointers to several other free blocks. The list head is in the superblock.
- Cheap to maintain — push/pop on allocation. Uses no extra disk space (blocks store the list while free).
- Hard to find contiguous runs (needed for reducing fragmentation).

**Bitmap**

- One bit per disk block: 1 = used, 0 = free. Stored in a fixed region of the disk.
- Trivially supports "find $N$ contiguous free blocks" — scan the bitmap for a run of zeros.
- Always-on cost: a 1TB disk with 4KB blocks needs $2^{28}$ bits = 32MB of bitmap.

# On-Disk Layout

- A typical disk's first block is the ==MBR== (master boot record), which contains [[boot|bootloader]] code and a partition table. Each partition holds an independent file system.

```
+-----+-------------+-------------+
| MBR | Partition 1 | Partition 2 | ...
+-----+-------------+-------------+

Partition layout:
+------------+------------+--------+--------+----------+----------------+
| Boot block | Superblock | Free   | Inodes | Root dir | Files and      |
|            |            | space  |        |          | directories    |
|            |            | bitmap |        |          |                |
+------------+------------+--------+--------+----------+----------------+
```

- ==Superblock==: a fixed-size header naming the locations and sizes of every other on-disk structure (where inodes start, where the bitmap is, where the data region begins). Read first on mount; everything else is found from it.

# Buffer Cache

- A region of kernel RAM that mirrors recently accessed disk blocks. Same role as the [[cache|CPU cache]] but at OS granularity (blocks instead of cache lines).
- Read path: check the cache; on miss, issue a disk read and install the block. Write path: modify the cached copy and mark it dirty; the OS flushes dirty blocks back to disk later.
- An LRU policy evicts the block whose most-recent reference is oldest. The cache turns the file system from disk-bound into RAM-bound for hot working sets.
- [[file systems|File systems]] keep multiple on-disk structures in sync (directory entry + inode + data blocks + free bitmap). A crash mid-update leaves them inconsistent. This note covers 
- the mechanisms that recover a consistent state after the failure.

# Crash Recovery

- A single high-level operation requires multiple disk writes. Deleting a file, for example:
	1. Remove the entry from the directory.
	2. Mark the inode free.
	3. Mark each data block free in the bitmap.
- The disk hardware writes one block at a time. Between any two of these writes, a crash leaves the file system in a halfway state — the directory says the file is gone, but the inode and blocks are still marked allocated. The bitmap, the inode table, and the directory disagree.
- Without recovery, every crash risks corruption. With unbounded use, eventually the file system becomes unreadable.

# Journaling

- A small, dedicated region of disk acts as a ==write-ahead log== for the file system.
- Every multi-step update follows this protocol:
	1. Write a journal entry describing every block-level change the operation will make. This is the ==intention==.
	2. Wait for the journal write to commit (reach disk).
	3. Apply the changes to the actual on-disk structures.
	4. Mark the journal entry as complete (or discard it).

- Crash analysis:
	- Crash before step 2: the journal entry is incomplete. On reboot, ignore it. The real FS has not been touched; everything is consistent.
	- Crash between steps 2 and 4: the journal entry is committed but the real FS may be partially updated. On reboot, ==replay== the journal entry — re-apply every change. The FS now matches the journal's intention.
	- Crash after step 4: nothing to do; both journal and FS are consistent.

- The journal is bounded and circular. Once an entry has been applied and acknowledged, its space is reclaimed for the next entry. Used by ext3, ext4, NTFS, HFS+.

# Idempotence

- Replay re-applies operations that may have already happened in part. Each operation must be ==idempotent== — running it twice produces the same result as running it once.
- Examples:
	- "Set bit $k$ in the free bitmap to 1" — idempotent. Setting a 1 to 1 is a no-op.
	- "Append block $k$ to the free list" — *not* idempotent. The block ends up in the list twice.
- Non-idempotent operations are made idempotent by adding a guard: "if not already present, append." Every journaled operation must pass this test or the recovery itself can corrupt the FS.

# Journal Modes

The choice of *what* to journal trades safety against write throughput.

**Writeback**

- Journal only metadata changes. Data blocks are written directly to their final location, possibly out of order with the metadata.
- Fast. After a crash, the metadata is consistent but a file's data may be stale or contain garbage from before the crash.

**Ordered**

- Journal only metadata, but force the data blocks to disk *before* committing the metadata journal entry.
- Slightly slower. After a crash, the metadata is consistent and points only to data that actually made it to disk. Old garbage cannot leak. Default for ext3/ext4.

**Data**

- Journal both metadata and data. Every block written twice — once to the journal, once to its final location.
- Safest. Slowest — write bandwidth roughly halved.

# Log-Structured Filesystem

- A radical alternative: the entire disk *is* the log. There is no separate "real FS" — all writes append to the end of the log.
- Mechanism:
	1. Buffer pending writes (data and metadata) in RAM.
	2. Periodically flush a single contiguous ==segment== to the end of the log on disk.
	3. Each segment header lists the inodes and data blocks it contains.
	4. A separate map structure says which segment holds the latest version of each inode.

- Wins:
	- All writes are sequential. No seek overhead. Closer to disk's peak bandwidth.
	- Crash recovery is built in — the log *is* the history. On reboot, scan from the last checkpoint forward and replay any complete entries.
- Cost: old versions of data accumulate. Overwriting a block leaves the old block as garbage somewhere in the log. A ==cleaner== thread continually scans the log's tail, discards garbage, and re-appends still-live data to the head.
- Used by JFFS2 (flash), F2FS. Conceptually influenced every modern FS even where not adopted directly.

# fsck

- The without-journal fallback. After a crash, scan the entire FS, check every consistency invariant (directory entries point to allocated inodes; allocated inodes are listed in the bitmap; reference counts match), and repair what can be repaired.
- Slow — proportional to the FS size, not the number of pending operations. A 1TB volume may take minutes to an hour. During that time the FS is offline.
- Used on FAT-style file systems with no journal. Modern journaled FSes still ship `fsck` as a fallback for damage that journaling cannot detect (bad blocks, bit rot) but it runs only on demand.