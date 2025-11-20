import pytest
from src.graph import Graph

class TestGraph:
    def test_graph_creation(self):
        edges = [(0, 1), (0, 2), (1, 2)]
        graph = Graph(3, edges)
        assert graph.n == 3
        assert graph.get_degree(0) == 2
        assert graph.get_degree(1) == 2
        assert graph.get_degree(2) == 2
    
    def test_invalid_vertex(self):
        edges = [(0, 1)]
        graph = Graph(2, edges)
        with pytest.raises(ValueError):
            graph.get_degree(5)
    
    def test_adjacency(self):
        edges = [(0, 1), (1, 2)]
        graph = Graph(3, edges)
        assert graph.is_adjacent(0, 1)
        assert graph.is_adjacent(1, 0)
        assert not graph.is_adjacent(0, 2)
    
    def test_max_degree(self):
        edges = [(0, 1), (0, 2), (1, 2), (1, 3)]
        graph = Graph(4, edges)
        assert graph.get_max_degree() == 3  # Vertex 1 has degree 3