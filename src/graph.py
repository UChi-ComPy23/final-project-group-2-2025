from typing import List, Tuple, Set, Dict, Optional
import numpy as np

class Graph:
    """
    Graph data structure implementation for graph coloring problems.
    """
    def __init__(self, vertices: int, edges: List[Tuple[int, int]]):
        """
        Initialize graph with vertices and edges.
        """
        self.n = vertices
        self.adjacency_list: Dict[int, Set[int]] = {i: set() for i in range(vertices)}
        self._build_adjacency_list(edges)
    
    def _build_adjacency_list(self, edges: List[Tuple[int, int]]) -> None:
        """
        Build adjacency list from edges.
        """
        for u, v in edges:
            if u < 0 or u >= self.n or v < 0 or v >= self.n:
                raise ValueError(f"Vertex index out of bounds: ({u}, {v})")
            self.adjacency_list[u].add(v)
            self.adjacency_list[v].add(u)
    
    def get_degree(self, vertex: int) -> int:
        """
        Get degree of a vertex.
        """
        if vertex not in self.adjacency_list:
            raise ValueError(f"Vertex {vertex} not in graph")
        return len(self.adjacency_list[vertex])
    
    def get_neighbors(self, vertex: int) -> Set[int]:
        """
        Get neighbors of a vertex.
        """
        if vertex not in self.adjacency_list:
            raise ValueError(f"Vertex {vertex} not in graph")
        return self.adjacency_list[vertex].copy()
    
    def is_adjacent(self, u: int, v: int) -> bool:
        """
        Check if two vertices are adjacent.
        """
        return v in self.adjacency_list[u]
    
    def get_max_degree(self) -> int:
        """
        Get maximum degree in the graph.
        """
        return max(len(neighbors) for neighbors in self.adjacency_list.values())
    
    def get_vertices(self) -> List[int]:
        """
        Get list of all vertices.
        """
        return list(range(self.n))
    
    def get_edges(self) -> List[Tuple[int, int]]:
        """
        Get list of all edges.
        """
        edges = set()
        for u, neighbors in self.adjacency_list.items():
            for v in neighbors:
                if u < v:  # Avoid duplicates
                    edges.add((u, v))
        return list(edges)
    
    def __str__(self) -> str:
        return f"Graph with {self.n} vertices and {len(self.get_edges())} edges"