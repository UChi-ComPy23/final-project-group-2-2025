from typing import List, Optional
import time
from .graph import Graph, is_proper_coloring


class GreedyResult:
    """
    A container to hold the results from the greedy coloring algorithm.
    
    This class stores information about what the greedy algorithm found,
    including the coloring solution, how many colors were used, and how long it took.
    """
    def __init__(
        self,
        coloring: Optional[List[int]],
        num_colors: int,
        time_seconds: float
    ):
        """
        Create a new result object.
        """
        self.coloring = coloring
        self.num_colors = num_colors
        self.time_seconds = time_seconds

    def __repr__(self):
        """
        Return a string representation of the result.
        """
        return (
            f"GreedyResult(num_colors={self.num_colors}, "
            f"time_seconds={self.time_seconds:.4f}s)"
        )


def greedy_coloring(graph: Graph, use_degree_order: bool = True) -> GreedyResult:
    """
    Color a graph using a simple greedy algorithm.
    
    This algorithm colors vertices one at a time. For each vertex, it picks the
    smallest color number (starting from 0) that hasn't been used by any of its
    neighbors. It's called "greedy" because it makes the best choice at each step
    without thinking about future consequences.
    """
    n = graph.n
    start_time = time.time()
    
    # Decide what order to color vertices in
    # If use_degree_order is True, we sort vertices by their degree (number of neighbors)
    # and color the ones with more neighbors first (this often gives better results)
    if use_degree_order:
        order = sorted(range(n), key=lambda v: graph.degree(v), reverse=True)
    else:
        # Otherwise, just color vertices in the order 0, 1, 2, ..., n-1
        order = list(range(n))
    
    # Initialize all vertices as uncolored (we use -1 to mean "no color yet")
    colors = [-1] * n
    
    # Color vertices one at a time in the chosen order
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
    
    # Count how many colors we used (colors are numbered 0, 1, 2, ..., so max + 1)
    num_colors = max(colors) + 1 if n > 0 else 0
    
    # Verify the coloring is proper (check that no two connected vertices have the same color)
    if not is_proper_coloring(graph, colors):
        return GreedyResult(None, -1, elapsed)
    
    return GreedyResult(
        coloring=colors,
        num_colors=num_colors,
        time_seconds=elapsed
    )

