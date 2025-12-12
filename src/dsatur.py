from typing import List, Optional, Set
import time
from .graph import Graph, is_proper_coloring


class DSATURResult:
    """
    A container to hold the results from the DSATUR algorithm.
    
    This class stores information about what the DSATUR algorithm found,
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
            f"DSATURResult(num_colors={self.num_colors}, "
            f"time_seconds={self.time_seconds:.4f}s)"
        )


def dsatur_coloring(graph: Graph) -> DSATURResult:
    """
    Color a graph using the DSATUR (Degree of Saturation) algorithm.
    
    DSATUR is a greedy algorithm that colors vertices one at a time. At each step,
    it picks the vertex with the highest "saturation" (how many different colors
    its neighbors already have). If there's a tie, it picks the vertex with the
    highest degree (most neighbors). This strategy often gives good results.
    """
    n = graph.n
    start_time = time.time()
    
    # Initialize all vertices as uncolored (we use -1 to mean "no color yet")
    colors = [-1] * n

    neighbor_colors: List[Set[int]] = [set() for _ in range(n)]
    
    # Color vertices one at a time until all are colored
    for _ in range(n):
        # Find the best vertex to color next
        best_vertex = -1
        best_saturation = -1
        best_degree = -1
        
        for v in range(n):
            if colors[v] != -1: 
                continue
            
            # Calculate saturation: how many different colors are used by neighbors
            saturation = len(neighbor_colors[v])
            # Get the degree: how many neighbors this vertex has
            degree = graph.degree(v)
            
            # Pick the vertex with highest saturation, or if tied, highest degree
            if saturation > best_saturation or \
               (saturation == best_saturation and degree > best_degree):
                best_vertex = v
                best_saturation = saturation
                best_degree = degree
 
        # If we couldn't find an uncolored vertex, we're done
        if best_vertex == -1:
            break
        
        v = best_vertex
        
        # Find the smallest color we can use for this vertex
        used_colors = neighbor_colors[v]
        color = 0
        # Keep trying colors until we find one that's not used by any neighbor
        while color in used_colors:
            color += 1
        
        colors[v] = color
        
        for neighbor in graph.adj[v]:
            neighbor_colors[neighbor].add(color)
    
    end_time = time.time()
    elapsed = end_time - start_time

    # Count how many colors we used (colors are numbered 0, 1, 2, ..., so max + 1)
    num_colors = max(colors) + 1 if n > 0 else 0
    
    # Verify the coloring is proper (should always be true for DSATUR, but check anyway)
    if not is_proper_coloring(graph, colors):
        return DSATURResult(None, -1, elapsed)
    
    return DSATURResult(
        coloring=colors,
        num_colors=num_colors,
        time_seconds=elapsed
    )

