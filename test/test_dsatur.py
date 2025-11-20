import pytest

from src.graph import Graph, is_proper_coloring
from src.dsatur import dsatur_coloring, DSATURResult


def test_dsatur_returns_result_object():
    """
    dsatur_coloring function should return a result object with the expected attributes.
    """
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)

    result = dsatur_coloring(g)

    assert isinstance(result, DSATURResult)
    assert hasattr(result, "coloring")
    assert hasattr(result, "num_colors")
    assert hasattr(result, "time_seconds")
    # Test __repr__ method
    repr_str = repr(result)
    assert "DSATURResult" in repr_str
    assert "num_colors" in repr_str


def test_dsatur_coloring():
    """
    Test DSATUR coloring produces valid coloring.
    """
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    result = dsatur_coloring(g)

    assert result.coloring is not None
    assert is_proper_coloring(g, result.coloring)
    # Path graph is 2-colorable
    assert result.num_colors == 2
    # Test triangle (K3) requires 3 colors
    g2 = Graph(3)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    g2.add_edge(2, 0)
    result2 = dsatur_coloring(g2)
    assert result2.coloring is not None
    assert is_proper_coloring(g2, result2.coloring)
    assert result2.num_colors == 3
