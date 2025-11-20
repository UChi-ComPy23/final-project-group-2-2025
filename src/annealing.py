import random
import math
import time
from typing import List, Optional
from .graph import Graph, is_proper_coloring


class SAResult:
    """
    Store simulated annealing result.
    """
    def __init__(self, coloring: Optional[List[int]], num_colors: int,
                 conflicts: int, time_seconds: float):
        self.coloring = coloring
        self.num_colors = num_colors
        self.conflicts = conflicts
        self.time_seconds = time_seconds

    def __repr__(self):
        return (f"SAResult(num_colors={self.num_colors}, "
                f"conflicts={self.conflicts}, "
                f"time_seconds={self.time_seconds:.4f}s)")


def count_conflicts(graph: Graph, colors: List[int]) -> int:
    """
    Count total conflicts.
    """
    conflicts = 0
    for u in range(graph.n):
        for v in graph.adj[u]:
            if colors[u] == colors[v]:
                conflicts += 1
    return conflicts // 2  # each counted twice


def simulated_annealing(graph: Graph, k: int,
                        max_iter: int = 20000,
                        T0: float = 1.0,
                        alpha: float = 0.999) -> SAResult:
    """
    Simulated annealing coloring with k colors.
    """
    n = graph.n
    start_time = time.time()

    # Initial random coloring
    colors = [random.randint(0, k - 1) for _ in range(n)]
    cur_conf = count_conflicts(graph, colors)

    T = T0

    for t in range(max_iter):

        # stop early if solved
        if cur_conf == 0:
            break

        # pick vertex and new color
        v = random.randint(0, n - 1)
        old_c = colors[v]
        new_c = random.randint(0, k - 1)
        while new_c == old_c:
            new_c = random.randint(0, k - 1)

        # compute new conflicts
        before = 0
        after = 0
        for u in graph.adj[v]:
            if colors[u] == old_c:
                before += 1
            if colors[u] == new_c:
                after += 1

        new_conf = cur_conf - before + after
        delta = new_conf - cur_conf

        # accept or reject
        if delta <= 0:
            colors[v] = new_c
            cur_conf = new_conf
        else:
            prob = math.exp(-delta / T)
            if random.random() < prob:
                colors[v] = new_c
                cur_conf = new_conf

        # cool down
        T *= alpha

    end_time = time.time()
    elapsed = end_time - start_time

    # check valid
    if cur_conf == 0 and is_proper_coloring(graph, colors):
        valid_coloring = colors.copy()
    else:
        valid_coloring = None

    return SAResult(valid_coloring, k, cur_conf, elapsed)
