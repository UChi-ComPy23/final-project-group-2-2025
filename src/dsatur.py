from typing import List, Optional, Set
import time
from .graph import Graph, is_proper_coloring


class DSATURResult:
    """
    Stores the result of the DSATUR coloring algorithm.
    """

    def __init__(
        self,
        coloring: Optional[List[int]],
        num_colors: int,
        time_seconds: float
    ):
        self.coloring = coloring
        self.num_colors = num_colors
        self.time_seconds = time_seconds

    def __repr__(self):
        return (
            f"DSATURResult(num_colors={self.num_colors}, "
            f"time_seconds={self.time_seconds:.4f}s)"
        )


def dsatur_coloring(graph: Graph) -> DSATURResult:
    """
    DSATUR (Degree of Saturation) graph coloring algorithm.
    """
    n = graph.n
    start_time = time.time()
    
    colors = [-1] * n

    neighbor_colors: List[Set[int]] = [set() for _ in range(n)]
    
    for _ in range(n):
        best_vertex = -1
        best_saturation = -1
        best_degree = -1
        
        for v in range(n):
            if colors[v] != -1: 
                continue
            
            saturation = len(neighbor_colors[v])
            degree = graph.degree(v)
            
            if saturation > best_saturation or \
               (saturation == best_saturation and degree > best_degree):
                best_vertex = v
                best_saturation = saturation
                best_degree = degree
 
        if best_vertex == -1:
            break
        
        v = best_vertex
        
        used_colors = neighbor_colors[v]
        color = 0
        while color in used_colors:
            color += 1
        
        colors[v] = color
        
        for neighbor in graph.adj[v]:
            neighbor_colors[neighbor].add(color)
    
    end_time = time.time()
    elapsed = end_time - start_time

    num_colors = max(colors) + 1 if n > 0 else 0
    
    # Verify the coloring is proper (should always be true for DSATUR)
    if not is_proper_coloring(graph, colors):
        return DSATURResult(None, -1, elapsed)
    
    return DSATURResult(
        coloring=colors,
        num_colors=num_colors,
        time_seconds=elapsed
    )

