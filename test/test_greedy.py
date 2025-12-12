import pytest

from src.graph import Graph, is_proper_coloring
from src.greedy import greedy_coloring, GreedyResult


def test_greedy_returns_result_object():
    """
    Test that the greedy_coloring function returns the correct type of result object.
    
    This test checks that the function returns a GreedyResult object and that
    this object has all the expected attributes (coloring, num_colors, time_seconds).
    It also checks that the string representation of the result works correctly.
    """
    # Create a simple path graph with 3 vertices: 0-1-2
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)

    # Run the greedy coloring algorithm
    result = greedy_coloring(g, use_degree_order=True)

    # Check that we got a GreedyResult object back
    assert isinstance(result, GreedyResult)
    # Check that the result has all the expected attributes
    assert hasattr(result, "coloring")
    assert hasattr(result, "num_colors")
    assert hasattr(result, "time_seconds")
    # Test that the string representation (what you see when you print it) works
    repr_str = repr(result)
    assert "GreedyResult" in repr_str
    assert "num_colors" in repr_str


def test_greedy_coloring():
    """
    Test that the greedy algorithm produces a valid coloring.
    
    This test checks that the greedy algorithm actually finds a proper coloring
    (no conflicts) and uses a reasonable number of colors. It tests both with
    and without degree ordering to make sure both options work.
    """
    # Create a path graph with 4 vertices: 0-1-2-3
    # A path graph can always be colored with 2 colors
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    # Run greedy coloring with degree ordering enabled
    result = greedy_coloring(g, use_degree_order=True)

    # Check that we got a valid coloring (not None)
    assert result.coloring is not None
    # Check that the coloring is proper (no conflicts)
    assert is_proper_coloring(g, result.coloring)
    # A path graph can be colored with 2 colors, so the algorithm should use 2
    assert result.num_colors == 2
    # Test with different ordering (without degree ordering)
    result2 = greedy_coloring(g, use_degree_order=False)
    # Should still get a valid coloring
    assert result2.coloring is not None
    assert is_proper_coloring(g, result2.coloring)
