from typing import List, Optional
import time
from .graph import Graph, is_proper_coloring


class GreedyResult:
    """
    Stores the result of the greedy coloring algorithm.
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
            f"GreedyResult(num_colors={self.num_colors}, "
            f"time_seconds={self.time_seconds:.4f}s)"
        )


def greedy_coloring(graph: Graph, use_degree_order: bool = True) -> GreedyResult:
    """
    Greedy graph coloring algorithm.
    """
    n = graph.n
    start_time = time.time()
    
    if use_degree_order:
        order = sorted(range(n), key=lambda v: graph.degree(v), reverse=True)
    else:
        order = list(range(n))
    
    colors = [-1] * n
    
    for v in order:
        used_colors = set()
        for neighbor in graph.adj[v]:
            if colors[neighbor] != -1:
                used_colors.add(colors[neighbor])
        
        color = 0
        while color in used_colors:
            color += 1
        
        colors[v] = color
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    num_colors = max(colors) + 1 if n > 0 else 0
    
    # Verify the coloring is proper
    if not is_proper_coloring(graph, colors):
        return GreedyResult(None, -1, elapsed)
    
    return GreedyResult(
        coloring=colors,
        num_colors=num_colors,
        time_seconds=elapsed
    )

