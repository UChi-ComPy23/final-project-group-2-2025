import pytest
import random
from src.graph import Graph, is_proper_coloring
from src.annealing import simulated_annealing, count_conflicts, SAResult


def test_count_conflicts_basic():
    """
    Test that the count_conflicts function correctly counts coloring conflicts.
    
    A conflict happens when two connected vertices have the same color. This test
    checks that the function correctly identifies conflicts and counts them properly.
    """
    # Create a path graph: 0-1-2
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)

    # Test with a coloring that has one conflict
    # Vertex 0 has color 0, vertex 1 has color 0 (conflict!), vertex 2 has color 1
    colors = [0, 0, 1]
    # There should be exactly 1 conflict (between vertices 0 and 1)
    assert count_conflicts(g, colors) == 1

    # Test with a coloring that has no conflicts
    # Vertex 0 has color 0, vertex 1 has color 1, vertex 2 has color 0
    colors = [0, 1, 0]
    # There should be 0 conflicts (all connected vertices have different colors)
    assert count_conflicts(g, colors) == 0


def test_sa_returns_result_object():
    """
    Test that the simulated_annealing function returns the correct type of result object.
    
    This test checks that the function returns a SAResult object and that
    this object has all the expected attributes (coloring, num_colors, conflicts, time_seconds).
    It also checks that the string representation of the result works correctly.
    """
    # Set a random seed so the test results are reproducible
    random.seed(0)
    # Create a simple path graph with 3 vertices: 0-1-2
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)

    # Run simulated annealing with 3 colors and 2000 iterations
    result = simulated_annealing(g, k=3, max_iter=2000)
    # Check that we got a SAResult object back
    assert isinstance(result, SAResult)
    # Check that the result has all the expected attributes
    assert hasattr(result, "coloring")
    assert hasattr(result, "num_colors")
    assert hasattr(result, "conflicts")
    assert hasattr(result, "time_seconds")
    # Test that the string representation (what you see when you print it) works
    repr_str = repr(result)
    assert "SAResult" in repr_str
    assert "num_colors" in repr_str


def test_sa_solves_easy_graph():
    """
    Test that simulated annealing can solve an easy graph when given enough colors.
    
    A path graph with 4 vertices can be colored with 2 colors. If we give simulated
    annealing 3 colors to work with, it should easily find a valid coloring (no conflicts).
    """
    # Set a random seed so the test results are reproducible
    random.seed(1)
    # Create a path graph with 4 vertices: 0-1-2-3
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    # Run simulated annealing with 3 colors (more than the 2 we actually need)
    result = simulated_annealing(g, k=3, max_iter=5000)

    # Since we have more colors than needed, we should find a valid coloring
    # Check that there are no conflicts
    assert result.conflicts == 0
    # Check that we got a valid coloring (not None)
    assert result.coloring is not None
    # Check that the coloring is proper (no conflicts)
    assert is_proper_coloring(g, result.coloring)


def test_sa_may_fail_when_k_too_small():
    """
    Test that simulated annealing fails when not given enough colors.
    
    A triangle graph (K3) requires 3 colors because all vertices are connected to each other.
    If we only give simulated annealing 2 colors, it should fail to find a valid coloring
    and report conflicts > 0.
    """
    # Set a random seed so the test results are reproducible
    random.seed(2)
    # Create a triangle: vertices 0, 1, 2 all connected to each other
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)  # triangle requires 3 colors (each vertex needs a different color)

    # Try to color with only 2 colors (not enough!)
    result = simulated_annealing(g, k=2, max_iter=3000)

    # Should have conflicts (can't color a triangle with only 2 colors)
    assert result.conflicts > 0
    # Should not have a valid coloring (coloring is None when conflicts > 0)
    assert result.coloring is None


def test_sa_proper_when_conflicts_zero():
    """
    Test that when simulated annealing reports zero conflicts, the coloring is actually proper.
    
    This test verifies that if simulated annealing says it found a solution with no conflicts,
    then the coloring it found is actually valid (passes the is_proper_coloring check).
    """
    # Set a random seed so the test results are reproducible
    random.seed(3)
    # Create a path graph with 5 vertices: 0-1-2-3-4
    g = Graph(5)
    edges = [(0,1), (1,2), (2,3), (3,4)]
    for u, v in edges:
        g.add_edge(u, v)

    # Run simulated annealing with 3 colors
    result = simulated_annealing(g, k=3, max_iter=3000)

    # If we found a coloring with zero conflicts, verify it's actually proper
    if result.coloring is not None:
        assert is_proper_coloring(g, result.coloring)
