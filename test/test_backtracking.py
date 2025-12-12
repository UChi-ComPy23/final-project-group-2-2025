import pytest

from src.graph import Graph, is_proper_coloring
from src.backtracking import backtracking_coloring, BacktrackingResult


def test_backtracking_returns_result_object():
    """
    Test that the backtracking_coloring function returns the correct type of result object.
    
    This test checks that the function returns a BacktrackingResult object and that
    this object has all the expected attributes (coloring, num_colors, nodes_visited, time_seconds).
    It also checks that the string representation of the result works correctly.
    """
    # Create a simple path graph with 3 vertices: 0-1-2
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)

    # Run the backtracking coloring algorithm
    result = backtracking_coloring(g, use_degree_order=True)

    # Check that we got a BacktrackingResult object back
    assert isinstance(result, BacktrackingResult)
    # Check that the result has all the expected attributes
    assert hasattr(result, "coloring")
    assert hasattr(result, "num_colors")
    assert hasattr(result, "nodes_visited")
    assert hasattr(result, "time_seconds")
    # Test that the string representation (what you see when you print it) works
    repr_str = repr(result)
    assert "BacktrackingResult" in repr_str
    assert "num_colors" in repr_str


def test_backtracking_solves_path_graph():
    """
    Test that backtracking finds the optimal coloring for a path graph.
    
    A path graph is a simple chain of vertices connected in a line. The backtracking
    algorithm should find that a path graph can be colored with exactly 2 colors,
    which is the minimum number needed.
    """
    # Create a path graph with 4 vertices: 0-1-2-3
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    result = backtracking_coloring(g, use_degree_order=True)

    # Check that we got a valid coloring (not None)
    assert result.coloring is not None
    # Check that the coloring is proper (no conflicts)
    assert is_proper_coloring(g, result.coloring)
    # The chromatic number (minimum colors needed) of a path graph is 2
    assert result.num_colors == 2


def test_backtracking_solves_triangle():
    """
    Test that backtracking finds the optimal coloring for a triangle graph.
    
    A triangle (also called K3) is a complete graph with 3 vertices where every
    vertex is connected to every other vertex. Since all vertices are connected,
    each one needs a different color, so we need exactly 3 colors.
    """
    # Create a triangle: vertices 0, 1, 2 all connected to each other
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)

    result = backtracking_coloring(g, use_degree_order=True)

    # Check that we got a valid coloring (not None)
    assert result.coloring is not None
    # Check that the coloring is proper (no conflicts)
    assert is_proper_coloring(g, result.coloring)
    # The chromatic number of K3 (triangle) is 3 (each vertex needs a different color)
    assert result.num_colors == 3


def test_backtracking_single_vertex():
    """
    Test that backtracking handles a graph with just one vertex correctly.
    
    A graph with a single vertex (and no edges) is the simplest case. It only
    needs 1 color since there are no edges to worry about.
    """
    # Create a graph with just one vertex (no edges)
    g = Graph(1)

    result = backtracking_coloring(g, use_degree_order=True)

    # Check that we got a valid coloring (not None)
    assert result.coloring is not None
    # Check that the coloring is proper (no conflicts, but there are no edges anyway)
    assert is_proper_coloring(g, result.coloring)
    # A single vertex with no edges needs exactly 1 color
    assert result.num_colors == 1


def test_backtracking_complete_graph_k4():
    """
    Test that backtracking finds the optimal coloring for a complete graph with 4 vertices.
    
    K4 is a complete graph where every vertex is connected to every other vertex.
    Since all vertices are connected to each other, each vertex needs a different color,
    so we need exactly 4 colors. This tests that backtracking can handle more complex graphs.
    """
    # Create K4: a complete graph with 4 vertices
    # This means we need to add an edge between every pair of vertices
    g = Graph(4)
    # Add all pairs of edges (every vertex connects to every other vertex)
    for u in range(4):
        for v in range(u + 1, 4):
            g.add_edge(u, v)

    result = backtracking_coloring(g, use_degree_order=True)

    # Check that we got a valid coloring (not None)
    assert result.coloring is not None
    # Check that the coloring is proper (no conflicts)
    assert is_proper_coloring(g, result.coloring)
    # The chromatic number of K4 is 4 (each vertex needs a different color)
    assert result.num_colors == 4