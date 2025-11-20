import random
from typing import List, Tuple
import numpy as np
from ..graph import Graph

def generate_random_graph(vertices: int, density: float) -> List[Tuple[int, int]]:
    """
    Generate random graph with specified density.
    """
    if density < 0 or density > 1:
        raise ValueError("Density must be between 0 and 1")
    
    max_edges = vertices * (vertices - 1) // 2
    target_edges = int(max_edges * density)
    
    # Generate all possible edges and sample
    possible_edges = [(i, j) for i in range(vertices) for j in range(i+1, vertices)]
    
    if target_edges >= len(possible_edges):
        return possible_edges
    else:
        return random.sample(possible_edges, target_edges)

def generate_complete_graph(vertices: int) -> List[Tuple[int, int]]:
    """
    Generate complete graph K_n.
    """
    return [(i, j) for i in range(vertices) for j in range(i+1, vertices)]

def generate_bipartite_graph(left_vertices: int, right_vertices: int, 
                           density: float = 1.0) -> List[Tuple[int, int]]:
    """
    Generate random bipartite graph.
    """
    edges = []
    for i in range(left_vertices):
        for j in range(left_vertices, left_vertices + right_vertices):
            if random.random() <= density:
                edges.append((i, j))
    return edges

def generate_cycle_graph(vertices: int) -> List[Tuple[int, int]]:
    """
    Generate cycle graph C_n.
    """
    edges = [(i, (i+1) % vertices) for i in range(vertices)]
    return edges

def generate_path_graph(vertices: int) -> List[Tuple[int, int]]:
    """
    Generate path graph P_n.
    """
    edges = [(i, i+1) for i in range(vertices-1)]
    return edges