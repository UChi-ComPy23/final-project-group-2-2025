from typing import Dict, Set
from src.base_class import ColoringAlgorithm
from src.graph import Graph

class DSATUR(ColoringAlgorithm):
    """
    DSATUR graph coloring algorithm.
    """
    def __init__(self, graph: Graph):
        """
        Initialize DSATUR algorithm.
        """
        super().__init__(graph)
        self.saturation: Dict[int, int] = {v: 0 for v in range(graph.n)}
        self.uncolored: Set[int] = set(range(graph.n))
    
    def _get_next_vertex(self) -> int:
        """
        Select next vertex to color using DSATUR heuristic.
        Returns the index of next vertex to color.
        """
        max_saturation = -1
        candidates = []
        
        # Find vertices with maximum saturation
        for vertex in self.uncolored:
            if self.saturation[vertex] > max_saturation:
                max_saturation = self.saturation[vertex]
                candidates = [vertex]
            elif self.saturation[vertex] == max_saturation:
                candidates.append(vertex)
        
        # Break ties by degree
        if len(candidates) == 1:
            return candidates[0]
        else:
            max_degree = -1
            selected = candidates[0]
            for vertex in candidates:
                degree = self.graph.get_degree(vertex)
                if degree > max_degree:
                    max_degree = degree
                    selected = vertex
            return selected
    
    def _update_saturation(self, vertex: int, color: int) -> None:
        """
        Update saturation degrees after coloring a vertex.
        """
        for neighbor in self.graph.get_neighbors(vertex):
            if neighbor in self.uncolored:
                # Check if this color is new for the neighbor's saturation
                neighbor_colors = set()
                for adj in self.graph.get_neighbors(neighbor):
                    if adj in self.coloring:
                        neighbor_colors.add(self.coloring[adj])
                
                self.saturation[neighbor] = len(neighbor_colors)
    
    def color(self) -> Dict[int, int]:
        """
        Execute DSATUR coloring algorithm.
        """
        self.coloring = {}
        self.saturation = {v: 0 for v in range(self.graph.n)}
        self.uncolored = set(range(self.graph.n))
        
        while self.uncolored:
            vertex = self._get_next_vertex()
            
            # Find available colors
            used_colors = set()
            for neighbor in self.graph.get_neighbors(vertex):
                if neighbor in self.coloring:
                    used_colors.add(self.coloring[neighbor])
            
            # Assign smallest available color
            color = 1
            while color in used_colors:
                color += 1
            
            self.coloring[vertex] = color
            self.uncolored.remove(vertex)
            self._update_saturation(vertex, color)
        
        return self.coloring