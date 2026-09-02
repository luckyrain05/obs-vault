- A ==greedy algorithm== builds a solution one step at a time, committing at each step to whatever choice looks best right now, and never revisiting that choice.
- Contrast with [[dp|DP]]: DP explores every subproblem outcome before combining the best ones. Greedy explores nothing — it picks once and moves on, which is why it's almost always faster when it applies.

# Greedy Choice Property

- A greedy algorithm only reaches the correct (globally optimal) answer if the problem has two properties.

**Greedy choice property**

- The locally optimal choice at each step is part of some globally optimal solution. Committing to it never has to be undone later.

**Optimal substructure**

- The optimal solution to the whole problem is built from the optimal solution to whatever subproblem remains after the greedy choice is removed.

- Without the greedy choice property, taking the locally best option can strand you somewhere no later choice can recover from:

```
coins = {1, 3, 4}, target = 6

Greedy (largest coin first): 4 + 1 + 1  → 3 coins
Optimal:                     3 + 3      → 2 coins
```

- This coin system isn't ==canonical==: a canonical coin system is one where always taking the largest coin ≤ the remaining amount is guaranteed optimal (e.g. standard currency: 1, 5, 10, 25).

# Activity Selection

- Given an [[arrays|array]] of `(start, end)` intervals, select the maximum number that don't overlap.

```python
def activity_selection(intervals):
	intervals.sort(key=lambda x: x[1])  # sort by end time
	count = 0
	last_end = float('-inf')

	for start, end in intervals:
		if start >= last_end:
			count += 1
			last_end = end

	return count
```

- `O(n log n)` TC, `O(1)` SC.

1. Sort intervals by end time — an interval that ends earlier leaves more room for whatever comes after it.
2. Track `last_end`, the end time of the most recently selected interval.
3. Walk the sorted intervals, selecting one only if its start is not before `last_end`.
4. Selecting an interval advances `last_end` to that interval's end.

`Notes:`

- Ending soonest always leaves the most room for whatever picks come after — this is the greedy choice property from the section above.

# Fractional Knapsack

- Given items with `(weight, value)` and a knapsack of fixed capacity, maximize total value taken. Items can be split into fractions.

```python
def fractional_knapsack(items, capacity):
	items.sort(key=lambda x: x[1] / x[0], reverse=True)  # sort by value/weight ratio, descending
	total_value = 0

	for weight, value in items:
		if capacity >= weight:
			capacity -= weight
			total_value += value
		else:
			total_value += value * (capacity / weight)
			break

	return total_value
```

- `O(n log n)` TC, `O(1)` SC.

1. Compute each item's ratio $\frac{v_i}{w_i}$ and sort descending.
2. Take whole items greedily while they fit in the remaining capacity.
3. When an item no longer fits whole, take the fraction of it that exactly fills the remaining capacity, then stop.

`Notes:`

- No later item has a better ratio, so stopping there is never suboptimal.
- 0/1 knapsack (items can't be split) does not have the greedy choice property — taking the best ratio first can strand capacity that a different combination would've used better. That variant needs [[dp]].
