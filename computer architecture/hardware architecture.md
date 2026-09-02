- There are two approaches to build circuits that can solve mathematical operations.
	1. Build unique [[logic gates]] for every unique operation, single use for every instruction, cannot process different or multiple instructions.
	2. ==Von Neumann model==, a obelisk consisting of two main units.
		1. Memory unit, storing operations that are to be read and executed.
		2. Processing unit, reads, executes, and writes the memory unit.
			- The memory unit can theoretically house any data. Thus, a single circuit can be reused to execute an indefinite amount of operations.

**Computers**

- All modern computer architecture is based around the Von Neumann model.
	1. A processing unit
	2. A memory unit
	3. A channel that allows the processing unit to read, execute, and write to the memory unit to complete mathematical operations.
- This is the very basic definitions of a computer. A fucking microwave is a computer.

# [[CPU]]

- A ==Central Processing Unit==, the processing unit in the Von Neumann model. 
- It reads executions from the memory unit and executes them.
- Capable of writing back to memory to modify its own data.

# [[ram]]

- ==Random access memory== is the memory unit in the Von Neumann model: any address readable in uniform time.
- RAM is too slow for the CPU alone; the next layer is [[cache]].

# [[Cache]]

- A small, fast memory embedded directly in the CPU that holds copies of recently accessed data from RAM. The RAM is still too slow, needs another layer.
- When the CPU needs data:
	1. Check the cache first.
	2. There is a chance that the data can be found in the cache, which is significantly faster to access than the RAM.
	3. Only when the request data does not exist in the cache, we check the RAM.
- Modern CPUs have multiple caching layers. Each larger but slower than the previous.

```
+-----+     +----------+     +----------+     +----------+     +-------+
| CPU | <-> | L1 Cache | <-> | L2 Cache | <-> | L3 Cache | <-> |  RAM  |
+-----+     +----------+     +----------+     +----------+     +-------+
~1 ns           ~1 ns            ~4 ns           ~10 ns          ~100 ns bytes           64 KB            256 KB          8 MB            16 GB
```

# GPU

- The Graphics Processing Unit is another computational unit, however completely separate from the CPU.
	- It is specifically designed for [[concurrency#N cores, N threads|parallel computing]]. Thousands of small cores optimized for doing the same operation on many pieces of data simultaneously.
- Originally built for rendering graphics (computing color values for millions of pixels in parallel), now used for any massively parallel workload, like AI training.

```
CPU: few cores, complex           GPU: thousands of cores, simple
+------+------+------+------+    +--+--+--+--+--+--+--+--+--+--+
| Core | Core | Core | Core |    |  |  |  |  |  |  |  |  |  |  |
|      |      |      |      |    +--+--+--+--+--+--+--+--+--+--+
+------+------+------+------+    |  |  |  |  |  |  |  |  |  |  |
                                 +--+--+--+--+--+--+--+--+--+--+
                                 |  |  |  |  |  |  |  |  |  |  |
                                 +--+--+--+--+--+--+--+--+--+--+
```

- The GPU has its own dedicated RAM called ==VRAM==. Data must be copied from system RAM to VRAM before the GPU can process it.
- Not part of a rudimentary computer, but essential for any modern system.

# Motherboard

- A very important piece of circuit board.
	- Physically holds the CPU and RAM and provide the bus connections.
	- Connects the power supply, GPU, external storage and devices, and all other necessary computer components with the CPU and RAM.
- Holds the data to instruct the computer on how to [[boot]].
