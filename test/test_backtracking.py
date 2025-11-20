import pytest

from src.graph import Graph, is_proper_coloring
from src.backtracking import backtracking_coloring, BacktrackingResult


def test_backtracking_returns_result_object():
    """
    backtracking_coloring function should return a result object with the expected attributes
    """
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)

    result = backtracking_coloring(g, use_degree_order=True)

    assert isinstance(result, BacktrackingResult)
    assert hasattr(result,"coloring")
    assert hasattr(result,"num_colors")
    assert hasattr(result,"nodes_visited")
    assert hasattr(result, "time_seconds")
    # Test __repr__ method
    repr_str = repr(result)
    assert "BacktrackingResult" in repr_str
    assert "num_colors" in repr_str


def test_backtracking_solves_path_graph():
    """
    Backtracking should find an 2-coloring for paths
    """
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    result = backtracking_coloring(g, use_degree_order=True)

    assert result.coloring is not None
    assert is_proper_coloring(g, result.coloring)
    #chromatic number ofpath is 2
    assert result.num_colors == 2


def test_backtracking_solves_triangle():
    """
    Backtracking should find exactly 3 colors for K3
    """
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)

    result = backtracking_coloring(g, use_degree_order=True)

    assert result.coloring is not None
    assert is_proper_coloring(g, result.coloring)
    # chromatic number of K3 is 3
    assert result.num_colors == 3


def test_backtracking_single_vertex():
    """
    a graph with a single vertex should use exactly 1 color.
    """
    g = Graph(1)

    result = backtracking_coloring(g, use_degree_order=True)

    assert result.coloring is not None
    assert is_proper_coloring(g, result.coloring)
    assert result.num_colors == 1


def test_backtracking_complete_graph_k4():
    """
    K4 requires 4 colors.
    """
    g = Graph(4)
    # add all pairs of edges
    for u in range(4):
        for v in range(u + 1, 4):
            g.add_edge(u, v)

    result = backtracking_coloring(g, use_degree_order=True)

    assert result.coloring is not None
    assert is_proper_coloring(g, result.coloring)
    # chromatic number of K4 is 4
    assert result.num_colors == 4