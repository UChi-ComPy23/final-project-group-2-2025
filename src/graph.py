from typing import List, Dict, Tuple


class Graph:
    """
    Simple undirected graph represented with adjacency lists.
    Vertices are labeled 0, 1, ..., n-1.
    """

    def __init__(self, n: int):
        """
        Create a graph with n vertices.
        """
        self.n = n
        self.adj: Dict[int, List[int]] = {i: [] for i in range(n)}

    def add_edge(self, u: int, v: int):
        """
        Add an undirected edge (u, v).
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
        Create a graph with n vertices and add edges from a list.
        """
        g = cls(n)
        for u, v in edges:
            g.add_edge(u, v)
        return g

    def degree(self, v: int) -> int:
        """
        Return the degree of vertex v.
        """
        return len(self.adj[v])


def is_proper_coloring(graph: Graph, colors: List[int]) -> bool:
    """
    Check whether a given coloring is proper:
    For every edge (u, v), we must have colors[u] != colors[v].
    """
    n = graph.n
    if len(colors) != n:
        return False

    for u in range(n):
        for v in graph.adj[u]:
            if colors[u] == colors[v]:
                return False

    return True
