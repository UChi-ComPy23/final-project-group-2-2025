import random
from .graph import Graph


def cycle_graph(n: int) -> Graph:
    """
    Create a cycle graph (ring topology).
    
    In a cycle graph, vertices are arranged in a circle where each vertex
    is connected to exactly two neighbors. The chromatic number is 2 if n is even,
    and 3 if n is odd.
    """
    g = Graph(n)
    # Connect each vertex to the next one, forming a ring
    for i in range(n):
        g.add_edge(i, (i + 1) % n) 
    return g


def complete_graph(n: int) -> Graph:
    """
    Create a complete graph (every vertex connected to every other vertex).
    
    In a complete graph, every pair of vertices is connected by an edge.
    The chromatic number equals n (each vertex needs a different color).
    """
    g = Graph(n)
    # Connect every vertex to every other vertex
    for u in range(n):
        for v in range(u + 1, n):
            g.add_edge(u, v)
    return g


def path_graph(n: int) -> Graph:
    """
    Create a path graph (linear chain).
    
    In a path graph, vertices are arranged in a line where each vertex
    (except the endpoints) is connected to exactly two neighbors.
    The chromatic number is always 2.
    """
    g = Graph(n)
    # Connect each vertex to the next one
    for i in range(n - 1):
        g.add_edge(i, i + 1)
    return g


def star_graph(n: int) -> Graph:
    """
    Create a star graph (hub and spoke topology).
    
    In a star graph, one central vertex is connected to all other vertices,
    but the outer vertices are not connected to each other.
    The chromatic number is 2 (center gets one color, all others get another).
    """
    g = Graph(n)
    # Connect vertex 0 (center) to all other vertices
    for i in range(1, n):
        g.add_edge(0, i)
    return g


def bipartite_graph(n: int, m: int, p: float = 1.0) -> Graph:
    """
    Create a bipartite graph (two sets of vertices).
    
    In a bipartite graph, vertices are divided into two groups, and edges
    only connect vertices from different groups. The chromatic number is 2.
    """
    g = Graph(n + m)
    # Connect vertices from first set to second set
    for u in range(n):
        for v in range(n, n + m):
            if random.random() < p:
                g.add_edge(u, v)
    return g


def random_graph(n: int, p: float) -> Graph:
    """
    Create a random graph using the Erdos-Rényi G(n,p) model.
    
    In this model, we start with n vertices and then for each pair of vertices,
    we add an edge between them with probability p. This creates graphs with
    different densities depending on the value of p.
    """
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                edges.append((u, v))
    return Graph.from_edge_list(n, edges)

