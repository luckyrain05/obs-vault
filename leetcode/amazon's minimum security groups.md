Given an integer [[arrays| array]] `security`, group the elements such that:

1. All elements in a group have the **same value**.
2. The sizes of **any two groups** differ by at most **1**.

Return the **minimum number of groups** needed.

# Solution

```python
def findMinimumGroups(security):
	# Represent subarrays as a dict 
    freq_hash = {}
    for value in security:
        freq_hash[value] = freq_hash.get(value, 0) + 1
    
    freq = list(freq_hash.values())
    max_allowed = min(freq) + 1
	 
	# try every max group size using i
    for i in range(max_allowed, 0, -1):
	    ans = 0
		impossible = False
		
	    for val in freq:
		    remainder = val % i
		    num = val // i
		    # remainder must be i - 1
		    if remainder != i - 1 or remainder != 0:
			    impossible = True
			    break
			    
			# i - 1 is allowed
			elif val = i - 1:
				best += 1
			
			# compute ans
			else:	
				ans += val // i
				if remainder = i - 1: ans += 1	
		
		if impossible = False: return ans
```

## TS Complexity

- `O(n) TC, O(n) SC`

## Explanation

1. We can represent the initial subarrays using a [[hashs#Dictionary|dictionary]], this makes finding the size of each much easier.
	1. We only care about the sizes of each, thus `list()` only needs the values.
2. We can't divide the smallest subarray by a bigger size. So smallest +1 is the biggest allowed subarray size, since we are allowed a difference of one.
3. Brute force every subarray size until we reach an answer.
	1. Start from biggest allowed size. Thus, when we eventually find a quotient, it is guaranteed to be the answer.
	2. `best <= n`, `n` being size of `security`.

## Notes

 - It may looks like a GCD problem. However, group sizes are allowed to differ by 1. 
 - Let `freq` be `[4, 10]`. The solution would be`[4, 5, 5]`, 3 subarrays. But the GCD would be 2, which wouldn't be helpful to reach the solution.
 - After the hashing optimization, we can only brute force.
