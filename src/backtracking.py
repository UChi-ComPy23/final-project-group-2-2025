from typing import List, Optional
import time
from .graph import Graph


class BacktrackingResult:
    """
    Stores the result of the backtracking coloring search.
    """

    def __init__(
        self,
        coloring: Optional[List[int]],
        num_colors: int,
        nodes_visited: int,
        time_seconds: float
    ):
        self.coloring = coloring
        self.num_colors = num_colors
        self.nodes_visited = nodes_visited
        self.time_seconds = time_seconds

    def __repr__(self):
        return (
            f"BacktrackingResult(num_colors={self.num_colors}, "
            f"nodes_visited={self.nodes_visited}, "
            f"time_seconds={self.time_seconds:.4f}s)"
        )


def backtracking_coloring(graph: Graph, use_degree_order: bool = True) -> BacktrackingResult:
    """
    Exact graph coloring with backtracking search.
    """
    n = graph.n

    if use_degree_order:
        order = sorted(range(n), key=lambda v: graph.degree(v), reverse=True)
    else:
        order = list(range(n))

    pos_of = {v: i for i, v in enumerate(order)}
    colors = [-1] * n

    best_coloring: Optional[List[int]] = None
    best_num_colors: int = n + 1 

    nodes_visited = 0
    start_time = time.time()

    def is_safe_vertex(v: int, c: int) -> bool:
        """
        Check if vertex v can be assigned color c.
        """
        for u in graph.adj[v]:
            if colors[u] == c:
                return False
        return True

    def dfs(cur_pos: int, used_colors: int):
        """
        recursive DFS for coloring (backtracking)
        """
        nonlocal best_coloring, best_num_colors, nodes_visited

        nodes_visited += 1

        # it's the best, stop
        if used_colors >= best_num_colors:
            return

        # all vertices are colored , end
        if cur_pos == n:
            best_num_colors = used_colors
            best_coloring = colors.copy()
            return

        v = order[cur_pos]

        # try existing colors first
        for c in range(used_colors):
            if is_safe_vertex(v, c):
                colors[v] = c
                dfs(cur_pos + 1, used_colors)
                colors[v] = -1  # backtrack

        # Try using a new color
        if is_safe_vertex(v, used_colors):
            colors[v] = used_colors
            dfs(cur_pos + 1, used_colors + 1)
            colors[v] = -1  # backtrack

    # Start DFS search
    dfs(cur_pos=0, used_colors=0)

    end_time = time.time()

    return BacktrackingResult(
        coloring=best_coloring,
        num_colors=best_num_colors if best_coloring is not None else -1,
        nodes_visited=nodes_visited,
        time_seconds=end_time - start_time
    )


