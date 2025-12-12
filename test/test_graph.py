import pytest

from src.graph import Graph, is_proper_coloring


def test_graph_init():
    """
    Test that we can create a new graph with a specific number of vertices.
    
    This test checks that when we create a graph with 5 vertices, it actually
    has 5 vertices, and each vertex has an empty list of neighbors to start with.
    """
    # Create a graph with 5 vertices
    g = Graph(5)
    # Check that the graph has exactly 5 vertices
    assert g.n == 5
    # Check that we have 5 adjacency lists (one for each vertex)
    assert len(g.adj) == 5
    # Check that each vertex from 0 to 4 exists and has no neighbors yet
    for i in range(5):
        assert i in g.adj
        assert g.adj[i] == []


def test_add_edge_basic():
    """
    Test that we can add edges between vertices correctly.
    
    This test checks that when we add an edge between two vertices, both vertices
    know about each other (since the graph is undirected). It also checks that
    we can't add an edge from a vertex to itself (self-loops are not allowed).
    """
    g = Graph(3)
    # Add an edge between vertex 0 and vertex 1
    g.add_edge(0, 1)
    
    # Check that vertex 0 knows vertex 1 is its neighbor
    assert 1 in g.adj[0]
    # Check that vertex 1 knows vertex 0 is its neighbor (undirected graph)
    assert 0 in g.adj[1]
    # Test that self-loops are not added (a vertex can't connect to itself)
    g.add_edge(2, 2)
    # Vertex 2 should not be in its own neighbor list
    assert 2 not in g.adj[2]


def test_degree():
    """
    Test that the degree function correctly counts how many neighbors a vertex has.
    
    The degree of a vertex is the number of edges connected to it. This test creates
    a graph where vertex 0 is connected to three other vertices, so it should have
    degree 3. The other vertices should have degree 1.
    """
    g = Graph(4)
    # Connect vertex 0 to vertices 1, 2, and 3
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    
    # Vertex 0 should have 3 neighbors, so degree is 3
    assert g.degree(0) == 3
    # Vertex 1 should have 1 neighbor (vertex 0), so degree is 1
    assert g.degree(1) == 1
    # Vertex 3 should have 1 neighbor (vertex 0), so degree is 1
    assert g.degree(3) == 1


def test_from_edge_list():
    """
    Test that we can create a graph from a list of edges.
    
    This is a convenient way to create a graph when we already know all the
    connections we want. This test creates a path graph: 0-1-2-3.
    """
    # Create a list of edges: (0,1), (1,2), (2,3)
    edges = [(0, 1), (1, 2), (2, 3)]
    # Create a graph with 4 vertices and add all these edges
    g = Graph.from_edge_list(4, edges)
    
    # Check that the graph has 4 vertices
    assert g.n == 4
    # Check that vertex 0 is connected to vertex 1
    assert 1 in g.adj[0]
    # Check that vertex 1 is connected to vertex 2
    assert 2 in g.adj[1]
    # Check that vertex 2 is connected to vertex 3
    assert 3 in g.adj[2]


def test_is_proper_coloring_valid():
    """
    Test that is_proper_coloring correctly identifies a valid coloring.
    
    A valid coloring means no two connected vertices have the same color.
    This test uses a simple path graph and a coloring where connected vertices
    have different colors, so it should return True.
    """
    g = Graph(3)
    # Create a path: 0-1-2
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    
    # Color vertex 0 with color 0, vertex 1 with color 1, vertex 2 with color 0
    # Since 0 and 1 have different colors, and 1 and 2 have different colors, this is valid
    colors = [0, 1, 0]
    assert is_proper_coloring(g, colors) is True


def test_is_proper_coloring_invalid():
    """
    Test that is_proper_coloring correctly identifies an invalid coloring.
    
    An invalid coloring has at least one edge where both endpoints have the same color.
    This test creates a coloring with a conflict and checks that the function returns False.
    It also tests that the function returns False if the coloring list has the wrong length.
    """
    g = Graph(3)
    # Create a path: 0-1-2
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    
    # Color vertex 0 with color 0, vertex 1 with color 0, vertex 2 with color 1
    # This is invalid because vertices 0 and 1 are connected but both have color 0
    colors = [0, 0, 1]
    assert is_proper_coloring(g, colors) is False
    # Test that the function returns False if we don't have enough colors (wrong length)
    assert is_proper_coloring(g, [0, 1]) is False
