Given an [[arrays|array]] of meeting time interval objects consisting of start and end times `[(start_1,end_1),(start_2,end_2),...(start_i < end_i)]`, determine if a person could add all meetings to their schedule without any conflicts.

**Note:** `(0,8)`, `(8,10)` is not considered a conflict at 8

# Solution

```python
def canAttendMeetings(self, intervals: List[Interval]) -> bool:
	intervals.sort(key = lambda x : x[0])
	
	for i in range(len(intervals) - 1):
		if intervals[i][1] > intervals[i+1][0]: return False 
		
	return True
```

## TS Complexity

- `O(n * log n)` TC, `O(1)` SC

## Explanation

## Notes

- Using [[array sorting]] to get chronological order.
- Everything else is obvious, only tricky thing here is lambda syntax.
