from typing import List, Optional
import time
from .graph import Graph


class BacktrackingResult:
    """
    A container to hold the results from the backtracking algorithm.
    
    This class stores all the important information about what the backtracking
    algorithm found, including the coloring solution, how many colors were used,
    how many nodes were explored, and how long it took.
    """

    def __init__(
        self,
        coloring: Optional[List[int]],
        num_colors: int,
        nodes_visited: int,
        time_seconds: float
    ):
        """
        Create a new result object.
        """
        self.coloring = coloring
        self.num_colors = num_colors
        self.nodes_visited = nodes_visited
        self.time_seconds = time_seconds

    def __repr__(self):
        """
        Return a string representation of the result.
        """
        return (
            f"BacktrackingResult(num_colors={self.num_colors}, "
            f"nodes_visited={self.nodes_visited}, "
            f"time_seconds={self.time_seconds:.4f}s)"
        )


def backtracking_coloring(graph: Graph, use_degree_order: bool = True) -> BacktrackingResult:
    """
    Find the minimum number of colors needed using backtracking search.
    
    This algorithm tries all possible ways to color the graph and finds the
    solution that uses the fewest colors. It uses backtracking, which means
    it tries a color assignment, and if it doesn't work, it goes back and
    tries something else.
    """
    n = graph.n

    # Decide what order to color vertices in
    # If use_degree_order is True, we sort vertices by their degree (number of neighbors)
    # and color the ones with more neighbors first (this often helps find solutions faster)
    if use_degree_order:
        order = sorted(range(n), key=lambda v: graph.degree(v), reverse=True)
    else:
        order = list(range(n))

    pos_of = {v: i for i, v in enumerate(order)}
    
    # Initialize all vertices as uncolored (we use -1 to mean "no color yet")
    colors = [-1] * n

    # Keep track of the best solution we've found so far
    best_coloring: Optional[List[int]] = None
    best_num_colors: int = n + 1

    # Count how many nodes we explore in the search tree
    nodes_visited = 0
    start_time = time.time()

    def is_safe_vertex(v: int, c: int) -> bool:
        """
        Check if we can assign color c to vertex v without causing a conflict.
        
        A conflict happens when two connected vertices have the same color.
        This function checks all neighbors of v to see if any of them already
        have color c.
        """
        for u in graph.adj[v]:
            # If a neighbor already has color c, we can't use c for v
            if colors[u] == c:
                return False
        # If no neighbor has color c, it's safe to use
        return True

    def dfs(cur_pos: int, used_colors: int):
        """
        Recursively search for a valid coloring using depth-first search.
        
        This function tries to color vertices one by one. For each vertex, it
        tries all possible colors. If a color works, it moves to the next vertex.
        If it gets stuck, it backtracks (goes back) and tries a different color.
        """
        nonlocal best_coloring, best_num_colors, nodes_visited

        nodes_visited += 1

        # If we're already using as many or more colors than our best solution,
        # there's no point continuing (we want to minimize colors)
        if used_colors >= best_num_colors:
            return

        # If we've colored all vertices, we found a complete solution!
        if cur_pos == n:
            best_num_colors = used_colors
            best_coloring = colors.copy()
            return

        # Get the vertex we're trying to color at this position
        v = order[cur_pos]

        # First, try using colors we've already used (this keeps the number of colors low)
        for c in range(used_colors):
            if is_safe_vertex(v, c):
                colors[v] = c
                dfs(cur_pos + 1, used_colors)
                colors[v] = -1

        # Also try using a brand new color (if it's safe)
        if is_safe_vertex(v, used_colors):
            colors[v] = used_colors
            dfs(cur_pos + 1, used_colors + 1)
            colors[v] = -1

    # Start the search from the beginning with no colors used yet
    dfs(cur_pos=0, used_colors=0)

    end_time = time.time()

    return BacktrackingResult(
        coloring=best_coloring,
        num_colors=best_num_colors if best_coloring is not None else -1,
        nodes_visited=nodes_visited,
        time_seconds=end_time - start_time
    )


