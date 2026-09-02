## Streams & Aggregations

**Moving average from data stream** — Compute a moving average over a fixed-size window of a stream.

**Running mean** — Compute the mean within a running list.

**Weighted average of past window** — Weighted average over the trailing window of a data stream.

**Median from data stream** — Maintain the median as elements stream in (two-heap solution).

**Merge k sorted lists** — https://leetcode.com/problems/merge-k-sorted-lists/ — framed as: you have K streams of data arriving in chronological order; combine them into one stream.

**Merge k lists, OOD variant** — Same idea but object-oriented, and the lists are **not guaranteed sorted**, so you can't just store the heads. You choose the underlying implementation (linked list vs array list).

**Sliding window** — Standard sliding window problem.

**Sliding window maximum** — Max within each window of a stream.

**Mean sliding window class** — Define a class computing a mean over a sliding window.

**Max sum within a time frame** — Maximum sum over a bounded time window.

**Subarray sum (maximum subarray)** — https://leetcode.com/problems/maximum-subarray/ — follow-up treats the array as **circular**.

**Sliding window → tree variant** — A list problem whose solution is a sliding window; then the same problem where the input is a **tree** instead of a list, requiring **2D DP**. Pseudocode/explanation accepted. (Note: there are 2 case types — solutions covering only one are incomplete.)

**k largest values** — Return the k largest values.

**First unique website visitor** — Data structure recording website visits supporting **O(1)** retrieval of the first visitor who has visited exactly once.

---

## Systems & Distributed Design

**Batch inference gateway (distributed queue)** — Researchers submit fire-and-forget jobs of millions of LLM inference requests and return hours later for results; jobs run 1–72h on cheap interruptible machines. Core design: dump input to blob storage, split into a durable queue, GPU workers pull/process/ack only after writing results, each result written independently keyed by `(job_id, index)` for idempotency and easy reassembly. Twist: diagnose a job stuck at **98% for 70 hours** that times out and discards everything — separate *"why is it stuck"* (limbo requests) from *"never discard already-completed work"* (finalize with partial results).

**Consistent hashing request router** — You're building a request router for a distributed key-value service. Each request has a string key; each backend server owns a subset of the keyspace. Implement a consistent hashing ring supporting: adding a node, removing a node, routing a key to the correct node, **virtual nodes** for load balance, and returning the next N distinct nodes for replication.

```python
class RingHashRouter:
    def __init__(self, replicas: int = 100): ...
    def add_node(self, node_id: str) -> None: ...
    def remove_node(self, node_id: str) -> None: ...
    def get_node(self, key: str) -> str: ...
    def get_nodes(self, key: str, count: int) -> list[str]: ...
```

**Broker with background reconnect** — A broker connecting to a server that reconnects in the background, with housekeeping for the packages that fail to send during the downtime.

**Kafka file parser** — Parse Kafka files.

**Rate limiter** — Design and implement a rate limiter.

**Server scheduling** — Standard server scheduling / task assignment problem.

**Unstructured → structured data pipeline** — AI-assisted: given a pile of unstructured data, design a pipeline converting it to structured, normalized data.

**Data ingestion class design** — Class design around data ingestion; follow-ups on **thread safety**.

**Data parsing question** — One data parsing problem paired with a separate OOD problem.

**Google Docs** — Design Google Docs (collaborative editing).

**SQL / tables** — Something basic related to SQL and table design.

**Trading system (open-ended)** — Build out a trading system from scratch; very open-ended, discussion-heavy, AI allowed.

**Trading game (open-ended)** — Build a "trading game"; so open-ended that candidate implementations diverge widely from what the interviewer had in mind.

**Drone allocation** — Open-ended: drone allocation for an Amazon-like delivery system.

**Claude Code wrapper** — Open-ended: design a simple wrapper around Claude Code.

**AI code review round** — Given a vague prompt, generate AI code, then walk through it together: do the functions do what's wanted/expected? Where is it inefficient, and which data structures fix it (heap instead of a list, companion hash map for O(1) lookup)? Heavy on time-complexity questions, then system design at the end: race conditions, concurrency, edge cases.
