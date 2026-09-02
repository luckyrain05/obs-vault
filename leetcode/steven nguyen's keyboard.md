A keyboard factory builds mechanical keyboard components in stages. Some parts are available from the start (base components), while others must be assembled using previously built components. Each keyboard component may depend on one or more other components, and it can only be built if all of its parts are available or can themselves be built.

Given an [[arrays|array]] of array of tuples, tuple(1) being the 

# Solution

```python
def building_keyboard(possible_components, base_components):
    graph = {}
    for construct, parts_list in possible_components:
        graph[construct] = parts_list
	
    buildable = set(base_components) # Parts confirmed buildable
    visiting = set()  # Components in current DFS path (cycle detection)
	
    def can_build(comp):
        if comp in buildable:
            return True
        if comp not in graph or comp in visiting:
            return False
		
		 visiting.add(comp)
		
        for part in graph[comp]:
            if not can_build(part):
                visiting.remove(comp)
                return False
		
        visiting.remove(comp)
        buildable.add(comp)
        return True
	
    result = []
    for comp in graph:
        if can_build(comp):
            result.append(comp)
	
    return result
```

## TS Complexity

- `O(v+e)` TC, `O(v+e)` SC.

## Explanation

1. Build a directed [[graphs|graph]] to represent the build progression
2. Then it is essentially checking for valid [[topological sort|topological sort]].

## Notes

