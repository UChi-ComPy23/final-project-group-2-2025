import pytest
import random
from src.graph import Graph, is_proper_coloring
from src.annealing import simulated_annealing, count_conflicts


def test_count_conflicts_basic():
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)

    colors = [0, 0, 1]  # only edge (0,1) conflicts
    assert count_conflicts(g, colors) == 1

    colors = [0, 1, 0]  # no conflicts
    assert count_conflicts(g, colors) == 0


def test_sa_returns_result_object():
    random.seed(0)
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)

    result = simulated_annealing(g, k=3, max_iter=2000)
    assert hasattr(result, "coloring")
    assert hasattr(result, "num_colors")
    assert hasattr(result, "conflicts")
    assert hasattr(result, "time_seconds")


def test_sa_solves_easy_graph():
    """
    A path graph of 4 nodes is 2-colorable.
    SA with k=3 should easily find a valid coloring.
    """
    random.seed(1)
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    result = simulated_annealing(g, k=3, max_iter=5000)

    # valid coloring expected
    assert result.conflicts == 0
    assert result.coloring is not None
    assert is_proper_coloring(g, result.coloring)


def test_sa_may_fail_when_k_too_small():
    """
    A triangle graph cannot be 2-colored.
    SA should fail with conflicts > 0 for k=2.
    """
    random.seed(2)
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)  # triangle requires 3 colors

    result = simulated_annealing(g, k=2, max_iter=3000)

    assert result.conflicts > 0
    assert result.coloring is None


def test_sa_proper_when_conflicts_zero():
    """
    If SA reports zero conflicts, coloring must be proper.
    """
    random.seed(3)
    g = Graph(5)
    edges = [(0,1),(1,2),(2,3),(3,4)]
    for u, v in edges:
        g.add_edge(u, v)

    result = simulated_annealing(g, k=3, max_iter=3000)

    if result.coloring is not None:
        assert is_proper_coloring(g, result.coloring)
