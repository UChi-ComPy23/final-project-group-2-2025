import time
from typing import Dict, List, Tuple, Any
import numpy as np
from src.graph import Graph
from src.greedy import GreedyColoring, generate_random_ordering
from src.dsatur import DSATUR

def analyze_coloring_quality(graph: Graph, coloring: Dict[int, int]) -> Dict[str, Any]:
    """
    Analyze quality of a coloring.
    """
    num_colors = len(set(coloring.values()))
    color_usage = {}
    for color in coloring.values():
        color_usage[color] = color_usage.get(color, 0) + 1
    
    return {
        'num_colors': num_colors,
        'color_usage': color_usage,
        'is_valid': is_valid_coloring(graph, coloring),
        'theoretical_lower_bound': graph.get_max_degree() + 1
    }

def is_valid_coloring(graph: Graph, coloring: Dict[int, int]) -> bool:
    """
    Check if coloring is valid.
    """
    for u in range(graph.n):
        for v in graph.get_neighbors(u):
            if coloring.get(u) == coloring.get(v):
                return False
    return True

def compare_algorithms(graph: Graph, num_trials: int = 100) -> Dict[str, Any]:
    """
    Compare performance of different coloring algorithms.
    """
    results = {}
    
    # Test DSATUR
    start_time = time.time()
    dsatur = DSATUR(graph)
    dsatur_coloring = dsatur.color()
    dsatur_time = time.time() - start_time
    
    results['dsatur'] = {
        'coloring': dsatur_coloring,
        'time': dsatur_time,
        'num_colors': dsatur.get_num_colors(),
        'is_valid': dsatur.is_valid_coloring()
    }
    
    # Test Greedy with multiple orderings
    greedy_results = []
    greedy_times = []
    
    for _ in range(num_trials):
        ordering = generate_random_ordering(graph.n)
        start_time = time.time()
        greedy = GreedyColoring(graph, ordering)
        greedy_coloring = greedy.color()
        greedy_times.append(time.time() - start_time)
        
        greedy_results.append({
            'num_colors': greedy.get_num_colors(),
            'is_valid': greedy.is_valid_coloring(),
            'ordering': ordering
        })
    
    color_counts = [r['num_colors'] for r in greedy_results]
    
    results['greedy_random'] = {
        'min_colors': np.min(color_counts),
        'max_colors': np.max(color_counts),
        'mean_colors': np.mean(color_counts),
        'std_colors': np.std(color_counts),
        'mean_time': np.mean(greedy_times),
        'all_results': greedy_results
    }
    
    # Test Greedy with degree ordering
    from src.greedy import generate_degree_ordering
    degree_ordering = generate_degree_ordering(graph)
    start_time = time.time()
    degree_greedy = GreedyColoring(graph, degree_ordering)
    degree_coloring = degree_greedy.color()
    degree_time = time.time() - start_time
    
    results['greedy_degree'] = {
        'coloring': degree_coloring,
        'time': degree_time,
        'num_colors': degree_greedy.get_num_colors(),
        'is_valid': degree_greedy.is_valid_coloring()
    }
    
    return results

def analyze_stability(graph: Graph, num_trials: int = 1000) -> Dict[str, Any]:
    """
    Analyze stability of greedy algorithm under random orderings.
    """
    color_counts = []
    
    for _ in range(num_trials):
        ordering = generate_random_ordering(graph.n)
        greedy = GreedyColoring(graph, ordering)
        coloring = greedy.color()
        color_counts.append(greedy.get_num_colors())
    
    color_counts = np.array(color_counts)
    
    return {
        'mean_colors': float(np.mean(color_counts)),
        'std_colors': float(np.std(color_counts)),
        'min_colors': int(np.min(color_counts)),
        'max_colors': int(np.max(color_counts)),
        'coefficient_of_variation': float(np.std(color_counts) / np.mean(color_counts)),
        'all_results': color_counts.tolist(),
        'histogram': np.histogram(color_counts, bins=range(min(color_counts), max(color_counts)+2))
    }