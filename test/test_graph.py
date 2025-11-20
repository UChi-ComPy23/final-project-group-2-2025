import pytest

from src.graph import Graph, is_proper_coloring


def test_graph_init():
    """
    Test Graph initialization with n vertices.
    """
    g = Graph(5)
    assert g.n == 5
    assert len(g.adj) == 5
    for i in range(5):
        assert i in g.adj
        assert g.adj[i] == []


def test_add_edge_basic():
    """
    Test adding a basic edge between two vertices (undirected).
    """
    g = Graph(3)
    g.add_edge(0, 1)
    
    assert 1 in g.adj[0]
    assert 0 in g.adj[1]
    # Test self-loops are not added
    g.add_edge(2, 2)
    assert 2 not in g.adj[2]


def test_degree():
    """
    Test degree calculation.
    """
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    
    assert g.degree(0) == 3
    assert g.degree(1) == 1
    assert g.degree(3) == 1  # vertex 3 has one edge


def test_from_edge_list():
    """
    Test creating graph from edge list.
    """
    edges = [(0, 1), (1, 2), (2, 3)]
    g = Graph.from_edge_list(4, edges)
    
    assert g.n == 4
    assert 1 in g.adj[0]
    assert 2 in g.adj[1]
    assert 3 in g.adj[2]


def test_is_proper_coloring_valid():
    """
    Test is_proper_coloring with a valid coloring.
    """
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    
    colors = [0, 1, 0]
    assert is_proper_coloring(g, colors) is True


def test_is_proper_coloring_invalid():
    """
    Test is_proper_coloring with an invalid coloring (conflict).
    """
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    
    colors = [0, 0, 1]  # conflict: 0 and 1 have same color but are adjacent
    assert is_proper_coloring(g, colors) is False
    # Test wrong length
    assert is_proper_coloring(g, [0, 1]) is False
