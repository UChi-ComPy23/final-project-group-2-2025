from abc import ABC, abstractmethod
from typing import Dict
from src.graph import Graph

class ColoringAlgorithm(ABC):
    """
    Base class for graph coloring algorithms.
    """
    def __init__(self, graph: Graph):
        """
        Initialize algorithm with graph.
        """
        self.graph = graph
        self.coloring: Dict[int, int] = {}
    
    @abstractmethod
    def color(self) -> Dict[int, int]:
        """
        Color the graph.
        """
        pass
    
    def get_coloring(self) -> Dict[int, int]:
        """
        Get the computed coloring.
        """
        return self.coloring.copy()
    
    def get_num_colors(self) -> int:
        """
        Get number of colors used in coloring.
        """
        return len(set(self.coloring.values()))
    
    def is_valid_coloring(self) -> bool:
        """
        Check if the coloring is valid.
        """
        for u in range(self.graph.n):
            for v in self.graph.get_neighbors(u):
                if self.coloring.get(u) == self.coloring.get(v):
                    return False
        return True