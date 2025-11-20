import pytest

from src.graph import Graph, is_proper_coloring
from src.greedy import greedy_coloring, GreedyResult


def test_greedy_returns_result_object():
    """
    greedy_coloring function should return a result object with the expected attributes.
    """
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)

    result = greedy_coloring(g, use_degree_order=True)

    assert isinstance(result, GreedyResult)
    assert hasattr(result, "coloring")
    assert hasattr(result, "num_colors")
    assert hasattr(result, "time_seconds")
    # Test __repr__ method
    repr_str = repr(result)
    assert "GreedyResult" in repr_str
    assert "num_colors" in repr_str


def test_greedy_coloring():
    """
    Test greedy coloring produces valid coloring.
    """
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    result = greedy_coloring(g, use_degree_order=True)

    assert result.coloring is not None
    assert is_proper_coloring(g, result.coloring)
    # Path graph is 2-colorable
    assert result.num_colors == 2
    # Test with different ordering
    result2 = greedy_coloring(g, use_degree_order=False)
    assert result2.coloring is not None
    assert is_proper_coloring(g, result2.coloring)
