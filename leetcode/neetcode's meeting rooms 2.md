Given an [[arrays|array]] of meeting time interval objects consisting of start and end times `[(start_1,end_1),(start_2,end_2),...,(start_i < end_i)]`, find the minimum number of rooms required to schedule all meetings without any conflicts.

**Note:** `(0,8),(8,10)` is **NOT** considered a conflict at 8.

# Solution

```python
import heapq

def minMeetingRooms(self, intervals: List[Interval]) -> int:
	intervals.sort(key = lambda x : x[0])
	heap = []
	
	for (start, end) in intervals:
		if heap and heap[0] <= start:
			heapq.heappop(heap)
		
		heapq.heappush(heap, end)
	
	return len(heap)
```

## TS Complexity

- `O(n * log n)` TC, `O(n)` SC.

## Explanation

1. Use [[array sorting]] for a chronological order.
2. Initiate a min [[heaps]] to store end times of meetings that require another room.
	-  A min heap would peek the earliest end time. If our start time is not after the earliest end time, don't bother checking the rest, we need a new room.
3. If start time is after meeting time, we can reuse the room stored at `heap[0]` currently. So we pop.
4. `len(heap)` should naturally be the number of rooms needed.

## Notes