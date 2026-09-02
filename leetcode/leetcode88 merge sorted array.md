You are given two integer [[arrays|arrays]] `nums1` and `nums2`, sorted in **non-decreasing order**, and two integers `m` and `n`, representing the number of elements in `nums1` and `nums2` respectively.

**Merge** `nums1` and `nums2` into a single array sorted in **non-decreasing order**.

The final sorted array should not be returned by the function, but instead be _stored inside the array_ `nums1`. To accommodate this, `nums1` has a length of `m + n`, where the first `m` elements denote the elements that should be merged, and the last `n` elements are set to `0` and should be ignored. `nums2` has a length of `n`.

# Solution

```python
def merge(nums1, m, nums2, n):
    i = m - 1      # pointer for nums1's actual elements
    j = n - 1      # pointer for nums2
    k = m + n - 1  # pointer for final position
    
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
```

## TS Complexity

- `O(m+n)` TC, `O(1)` SC.

## Explanation

## Notes

- Study up on [[array sorting|sorting algorithms]]. The solution is simply a modified step of merge sort.



