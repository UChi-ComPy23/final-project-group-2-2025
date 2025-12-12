import random
import math
import time
from typing import List, Optional
from .graph import Graph, is_proper_coloring


class SAResult:
    """
    A container to hold the results from the simulated annealing algorithm.
    
    This class stores information about what the simulated annealing algorithm
    found, including the coloring solution, how many colors were used, how many
    conflicts (errors) remain, and how long it took.
    """
    def __init__(self, coloring: Optional[List[int]], num_colors: int,
                 conflicts: int, time_seconds: float):
        """
        Create a new result object.
        """
        self.coloring = coloring
        self.num_colors = num_colors
        self.conflicts = conflicts
        self.time_seconds = time_seconds

    def __repr__(self):
        """
        Return a string representation of the result.
        """
        return (f"SAResult(num_colors={self.num_colors}, "
                f"conflicts={self.conflicts}, "
                f"time_seconds={self.time_seconds:.4f}s)")


def count_conflicts(graph: Graph, colors: List[int]) -> int:
    """
    Count how many conflicts (errors) there are in a coloring.
    
    A conflict happens when two connected vertices have the same color. This
    function goes through all edges and counts how many have this problem.
    """
    conflicts = 0
    # Check every vertex and all its neighbors
    for u in range(graph.n):
        for v in graph.adj[u]:
            # If two connected vertices have the same color, that's a conflict
            if colors[u] == colors[v]:
                conflicts += 1
    # We count each edge twice (once from each endpoint), so divide by 2
    return conflicts // 2


def simulated_annealing(graph: Graph, k: int,
                        max_iter: int = 20000,
                        T0: float = 1.0,
                        alpha: float = 0.999) -> SAResult:
    """
    Try to color a graph using simulated annealing with k colors.
    
    Simulated annealing is inspired by how metal cools down. It starts with a
    random coloring and makes small random changes. It always accepts changes
    that make things better, and sometimes accepts changes that make things
    worse (especially early on). As it "cools down", it becomes less likely
    to accept bad changes.
    """
    n = graph.n
    start_time = time.time()

    # Start with a random coloring: assign each vertex a random color from 0 to k-1
    colors = [random.randint(0, k - 1) for _ in range(n)]
    cur_conf = count_conflicts(graph, colors)

    # Initialize the temperature (starts high, will decrease over time)
    T = T0

    for t in range(max_iter):

        # If we found a valid solution (no conflicts), we can stop early
        if cur_conf == 0:
            break

        # Pick a random vertex and a random new color for it
        v = random.randint(0, n - 1)
        old_c = colors[v]
        new_c = random.randint(0, k - 1)
        # Make sure the new color is different from the old one
        while new_c == old_c:
            new_c = random.randint(0, k - 1)

        # Calculate how many conflicts we'd have if we make this change
        # We only need to check neighbors of v, since only edges involving v can change
        before = 0 
        after = 0  
        for u in graph.adj[v]:
            if colors[u] == old_c:
                before += 1  
            if colors[u] == new_c:
                after += 1  

        # Calculate the new total number of conflicts
        new_conf = cur_conf - before + after
        delta = new_conf - cur_conf

        # Decide whether to accept this change
        if delta <= 0:
            colors[v] = new_c
            cur_conf = new_conf
        else:
            # The change makes things worse, but we might still accept it
            # The probability of accepting decreases as temperature decreases
            prob = math.exp(-delta / T)
            if random.random() < prob:
                colors[v] = new_c
                cur_conf = new_conf

        T *= alpha

    end_time = time.time()
    elapsed = end_time - start_time

    # Check if we found a valid solution (no conflicts and passes validation)
    if cur_conf == 0 and is_proper_coloring(graph, colors):
        valid_coloring = colors.copy()
    else:
        valid_coloring = None

    return SAResult(valid_coloring, k, cur_conf, elapsed)
