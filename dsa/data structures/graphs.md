
- A graph is just a bunch of ==nodes==, or points, connected by ==edges==, or lines.
- It is purely conceptual. Any data structure that behaves as if traveling from point to point through predetermined paths are graphs.

# Edge Direction

**Directed graphs**:

- Directed graph edges have a direction.
- No guarantee that it is possible to visit every node starting from one node.
- To visit every node, attempt visit all neighbors recursively from every node.

**Undirected Graphs**:

- Edges do not have a direction.
- To visit every node, simply visit all neighbors recursively from one node.
- Other qualities are then intuitive.

# Topological Order

- A graph has a topological order if for every series of traversals, it is impossible to revisit any previously visited node.
- A graph with a topological order is an ==Acyclic Graph==, or Directed Acyclic Graph (DAG) when directed.

# Cycles

- A cycle is a series of nodes, either directed or undirected, when traversed revisits one or more nodes.
- An acyclic graph has zero cycles. 

# [[arrays|Array]] Implementation

# [[hashs#Dictionary|Dictionary]] Implementation

# [[linked lists]] Implementation