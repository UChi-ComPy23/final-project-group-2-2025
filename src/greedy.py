import random
from typing import List, Dict, Optional
from src.base_class import ColoringAlgorithm
from src.graph import Graph

class GreedyColoring(ColoringAlgorithm):
    """
    Greedy coloring algorithm with customizable ordering.
    """
    def __init__(self, graph: Graph, ordering: Optional[List[int]] = None):
        """
        Initialize greedy coloring algorithm.
        """
        super().__init__(graph)
        self.ordering = ordering or list(range(graph.n))
    
    def color(self) -> Dict[int, int]:
        """
        Execute greedy coloring algorithm.
        """
        self.coloring = {}
        
        for vertex in self.ordering:
            # Find colors used by neighbors
            used_colors = set()
            for neighbor in self.graph.get_neighbors(vertex):
                if neighbor in self.coloring:
                    used_colors.add(self.coloring[neighbor])
            
            # Assign smallest available color
            color = 1
            while color in used_colors:
                color += 1
            
            self.coloring[vertex] = color
        
        return self.coloring

def generate_random_ordering(n: int) -> List[int]:
    """
    Generate random vertex ordering.
    """
    ordering = list(range(n))
    random.shuffle(ordering)
    return ordering

def generate_degree_ordering(graph: Graph, descending: bool = True) -> List[int]:
    """
    Generate vertex ordering by degree.
    """
    vertices = list(range(graph.n))
    vertices.sort(key=lambda v: graph.get_degree(v), reverse=descending)
    return vertices

def generate_largest_first_ordering(graph: Graph) -> List[int]:
    """
    Generate largest-first ordering (decreasing degree).
    """
    return generate_degree_ordering(graph, descending=True)

def generate_smallest_last_ordering(graph: Graph) -> List[int]:
    """
    Generate smallest-last ordering.
    """
    return generate_degree_ordering(graph, descending=False)