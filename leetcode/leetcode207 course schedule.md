There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an [[arrays|array]] `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you **must** take course `bi` first if you want to take course `ai`.

- For example, the pair `[0, 1]`, indicates that to take course `0` you have to first take course `1`.

Return `true` if you can finish all courses. Otherwise, return `false`.

# Solution

```python
def canFinish(numCourses, prerequisites):
    # Build adjacency list
    adj = [[] for _ in range(numCourses)]

    for course, prereq in prerequisites:
        adj[prereq].append(course)

    visiting = set()  # Nodes in current DFS path
    visited = set()   # Nodes completely processed

    def dfs(course):
        if course in visiting:
            return False  # Cycle detected
        if course in visited:
            return True   # Already processed

        visiting.add(course)

        for neighbor in adj[course]:
            if not dfs(neighbor):
                return False

        visiting.remove(course)
        visited.add(course)
        return True

    for course in range(numCourses):
        if not dfs(course):
            return False

    return True
```

## TS Complexity

- `O(v+e)` TC, `O(v+e)` SC.

## Explanation

1. This is simply [[topological sort|topological sort]] if we build a dependency [[graphs#Nodes and Edges|graph]] from the arrays.

## Notes
