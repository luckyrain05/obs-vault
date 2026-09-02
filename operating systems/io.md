- The OS mediates every interaction between programs and hardware peripherals (disks, keyboards, network cards, etc.). Hardware is shared and timing-sensitive; the kernel hides those details behind uniform `read`/`write` interfaces.
- Three policies — polling, interrupt-driven, DMA — trade CPU work against latency. The choice depends on how often the device produces data and how much.

# Devices and Controllers

- A peripheral is mechanical (the spinning platter, the keys, the antenna) plus a ==device controller== (the electronic component that drives it). The OS talks to the controller; the controller talks to the mechanism.
- The controller exposes a small set of hardware registers: ==command== (what to do), ==data== (bytes to transfer), ==status== (busy/error/ready). The OS reads and writes these registers to issue requests and observe results.

**Block device**

- Random access in fixed-size units (typically 512B or 4KB). Any block is as cheap to read as any other.
- Examples: hard disk, SSD, CD-ROM.

**Character device**

- Streamed bytes. No structured blocks; reads consume in order.
- Examples: keyboard, serial port, mouse.

# Talking to a Controller

**Port I/O**

- A separate address space for device registers, accessed by dedicated CPU instructions (`in`, `out` on x86).
- `in REG, PORT` reads from a port; `out PORT, REG` writes. Privileged — only kernel code can execute them.

**Memory-mapped I/O** (MMIO)

- Device registers are mapped into the same physical address space as RAM. Reading or writing a designated address has the side effect of reading or writing the device.
- Same `mov` instructions as for memory. The OS sets up page table entries that mark the MMIO range non-cacheable so that loads and stores actually reach the device instead of being absorbed by the [[cache]].

# Programming Models

The CPU's role in moving data between the controller and main memory.

**Polling** (programmed I/O)

- CPU loops on the status register until the device is ready, then transfers a byte or a word, then loops again.

```c
void read_debug_char(int *c) {
    while ((status_register & READY) == 0) ;   // busy-wait
    *c = data_register;
}
```

- Simple. CPU is fully occupied during the wait — the entire core does no useful work while the device is slow.

**Interrupt-driven I/O**

- CPU issues the request and goes off to do other work. When the device is ready, it raises a [[software interrupt#Interrupt Controller|hardware interrupt]]. The handler reads the data, possibly schedules another transfer.
- One interrupt per byte or word transferred. Fine for slow, sporadic devices (keyboard, mouse). Costly for high-bandwidth ones — the interrupt overhead per byte dominates.

**DMA** (direct memory access)

- A separate ==DMA controller== chip transfers data between the device and main memory without the CPU in the loop. The CPU programs the DMA controller once (source, destination, count) and is interrupted only when the entire transfer is complete.

```
1. CPU writes source, dest, length into DMA controller registers.
2. CPU starts the transfer and resumes other work.
3. DMA controller arbitrates for the bus, moves bytes between device
   and RAM until the count is reached.
4. DMA controller raises one interrupt: "done."
5. CPU's handler acknowledges, hands the data to the requester.
```

- One interrupt for an arbitrarily large transfer. Required for disk and network at modern speeds.

# Device Drivers

- A ==device driver== is the piece of kernel code that knows the specifics of one controller model. It translates generic OS requests ("read block N") into the register pokes and bus transactions that controller demands.
- Responsibilities:
	- Initialization at boot (or hot-plug): bring the device into a known state.
	- Control: accept requests from higher OS layers, issue them to the controller.
	- Multiplexing: queue requests if the device is busy.
	- Power management: idle the device when unused.
- Drivers conform to a kernel-defined ==driver API== so the OS can swap one disk driver for another without changing the file-system layer above. Manufacturers write drivers against this [[api|API]].

# Interrupt Handler Structure

- An interrupt handler that does heavy work blocks further interrupts and risks dropping events from a fast device. Linux splits handlers in two:

**Top half**

- Runs with interrupts disabled. Acknowledges the interrupt (so the controller can deliver the next), grabs the data out of the device's registers, queues a deferred-work item.
- Must be short — milliseconds matter at 10Gbps.

**Bottom half**

- Runs later, with interrupts enabled. Processes queued work: copies the data to the user buffer, wakes any thread blocked on the read, frees buffers.
- Lower priority; can be preempted by another top-half firing.

# Buffering

- Devices and processes operate at different rates and granularities. The kernel buffers transfers to bridge the gap.

**Single buffer**

- One kernel buffer. Device fills it; kernel copies to user space. New device data must wait until the copy completes.

**Double buffer**

- Two kernel buffers. While one is being copied to user space, the device fills the other. They swap when full. The device never has to wait.

**Ring buffer**

- A circular array with two pointers: ==head== (next write position) and ==tail== (next read position). Producer advances head; consumer advances tail; both wrap modulo the buffer size.
- Used for streams of unbounded length: network packets, keystrokes. Producer and consumer run at independent rates as long as the ring does not fill (overflow → dropped data) or empty (underflow → reader blocks).
