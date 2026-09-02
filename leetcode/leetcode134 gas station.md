There are `n` gas stations along a circular route, where the amount of gas at the `ith` station is `gas[i]`.

You have a car with an unlimited gas tank and it costs `cost[i]` of gas to travel from the `ith` station to its next `(i + 1)th` station. You begin the journey with an empty tank at one of the gas stations.

Given two integer arrays `gas` and `cost`, return _the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return_ `-1`. If there exists a solution, it is **guaranteed** to be **unique**.

# Solution

```Python
def canCompleteCircuit(gas: List[int], cost: List[int]) -> int:
	if sum(gas) < sum(cost): 
		return -1
	
	start = tank = 0	
	for i in range(len(gas)):
		tank = gas[i] - cost[i]
		
		if tank < 0:
			start = i + 1
			tank = 0
	
	return start
```

## TS Complexity

`O(n)` TC, `O(n)` SC

## Explanation

1. If total gas is less than total cost, it is impossible to complete the trip. Vice versa is true, if total gas is more or equal to total cost, there will always be a solution.
2. The main observation is that, say we start on index `s` (initially 0), and we run out of gas on index `i`, we can provably know that we can travel from `s` to `i` on an empty tank, with not enough juice to get to `i+1`.
3. So then, test again with `s` = `i+1`. If we make it to the end of the [[arrays|array]], we know that we can travel from the new `s` to the end, and from 0 to the last stop, making a complete circuit.
4. Even if we do not make it to the end, maybe we cannot move at all. But our initial sum calculation proves that there has to be a solution. So just keep testing one block forward until we can find where all the gas is.

## Notes

- This is a [[greedy]] solution.