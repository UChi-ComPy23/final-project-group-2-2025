from typing import List, Dict, Tuple


class Graph:
    """
    A simple graph class to represent graphs for coloring problems.
    
    This graph stores connections between vertices (nodes). Each vertex has a number
    from 0 to n-1, and we keep track of which vertices are connected to each other.
    """

    def __init__(self, n: int):
        """
        Create a new empty graph with n vertices.
        """
        self.n = n
        self.adj: Dict[int, List[int]] = {i: [] for i in range(n)}

    def add_edge(self, u: int, v: int):
        """
        Add a connection (edge) between two vertices.
        
        Since this is an undirected graph, if we connect u to v, then v is also
        connected to u. We don't allow a vertex to be connected to itself.
        """
        if u == v:
            return
        if v not in self.adj[u]:
            self.adj[u].append(v)
        if u not in self.adj[v]:
            self.adj[v].append(u)

    @classmethod
    def from_edge_list(cls, n: int, edges: List[Tuple[int, int]]):
        """
        Create a graph from a list of edges.
        
        This is a convenient way to create a graph when you already know all the
        connections you want to make.
        """
        g = cls(n)
        for u, v in edges:
            g.add_edge(u, v)
        return g

    def degree(self, v: int) -> int:
        """
        Count how many neighbors a vertex has.
        
        The degree of a vertex is the number of edges connected to it.
        """
        return len(self.adj[v])


def is_proper_coloring(graph: Graph, colors: List[int]) -> bool:
    """
    Check if a coloring is valid (proper).
    
    A proper coloring means that no two connected vertices have the same color.
    This function checks every edge in the graph to make sure the two vertices
    connected by that edge have different colors.
    """
    n = graph.n
    # First check: we need exactly one color for each vertex
    if len(colors) != n:
        return False

    # Check every vertex and all its neighbors
    for u in range(n):
        for v in graph.adj[u]:
            # If two connected vertices have the same color, it's not proper
            if colors[u] == colors[v]:
                return False

    # If we made it here, all edges have different colors on their endpoints
    return True
