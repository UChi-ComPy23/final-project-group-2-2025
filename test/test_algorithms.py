import pytest
from src.graph import Graph
from src.greedy import GreedyColoring, generate_random_ordering
from src.dsatur import DSATUR
from src.metrics import is_valid_coloring

class TestGreedyColoring:
    def test_greedy_coloring(self):
        edges = [(0, 1), (1, 2), (2, 0)]  # Triangle
        graph = Graph(3, edges)
        greedy = GreedyColoring(graph)
        coloring = greedy.color()
        
        assert is_valid_coloring(graph, coloring)
        assert greedy.get_num_colors() == 3
    
    def test_greedy_with_ordering(self):
        edges = [(0, 1), (1, 2)]
        graph = Graph(3, edges)
        ordering = [2, 1, 0]  # Custom ordering
        greedy = GreedyColoring(graph, ordering)
        coloring = greedy.color()
        
        assert is_valid_coloring(graph, coloring)
        assert greedy.get_num_colors() == 2

class TestDSATUR:
    def test_dsatur_coloring(self):
        edges = [(0, 1), (1, 2), (2, 0)]  # Triangle
        graph = Graph(3, edges)
        dsatur = DSATUR(graph)
        coloring = dsatur.color()
        
        assert is_valid_coloring(graph, coloring)
        assert dsatur.get_num_colors() == 3
    
    def test_dsatur_bipartite(self):
        edges = [(0, 2), (0, 3), (1, 2), (1, 3)]  # K_{2,2}
        graph = Graph(4, edges)
        dsatur = DSATUR(graph)
        coloring = dsatur.color()
        
        assert is_valid_coloring(graph, coloring)
        assert dsatur.get_num_colors() == 2