from typing import List, Dict
from .graph import Graph
from .backtracking import backtracking_coloring
from .greedy import greedy_coloring
from .dsatur import dsatur_coloring
from .annealing import simulated_annealing
from .graph_generators import (
    cycle_graph, complete_graph, path_graph, star_graph,
    bipartite_graph, random_graph
)


def compare_all_algorithms(graph: Graph, k_for_annealing: int = None) -> Dict:
    """
    Run all four algorithms on the same graph and compare results.
    
    This function runs backtracking, greedy, DSATUR, and simulated annealing
    on the same graph and collects their results for comparison.
    
    Note: Simulated annealing requires a fixed number of colors k. If k_for_annealing
    is None, we first run the other algorithms to find the minimum number of colors,
    then use that for simulated annealing.
    """
    results = {}
    
    # Run backtracking (finds optimal/minimum number of colors)
    try:
        backtrack_result = backtracking_coloring(graph, use_degree_order=True)
        results['backtracking'] = {
            'coloring': backtrack_result.coloring,
            'num_colors': backtrack_result.num_colors,
            'time': backtrack_result.time_seconds,
            'nodes_visited': backtrack_result.nodes_visited,
            'success': backtrack_result.coloring is not None
        }
    except Exception as e:
        results['backtracking'] = {'error': str(e), 'success': False}
    
    # Run greedy
    try:
        greedy_result = greedy_coloring(graph, use_degree_order=True)
        results['greedy'] = {
            'coloring': greedy_result.coloring,
            'num_colors': greedy_result.num_colors,
            'time': greedy_result.time_seconds,
            'success': greedy_result.coloring is not None
        }
    except Exception as e:
        results['greedy'] = {'error': str(e), 'success': False}
    
    # Run DSATUR
    try:
        dsatur_result = dsatur_coloring(graph)
        results['dsatur'] = {
            'coloring': dsatur_result.coloring,
            'num_colors': dsatur_result.num_colors,
            'time': dsatur_result.time_seconds,
            'success': dsatur_result.coloring is not None
        }
    except Exception as e:
        results['dsatur'] = {'error': str(e), 'success': False}
    
    # Determine k for simulated annealing
    # Use the minimum number of colors found by other algorithms, or provided k
    if k_for_annealing is None:
        # Find the minimum number of colors from successful algorithms
        min_colors = None
        for alg in ['backtracking', 'greedy', 'dsatur']:
            if alg in results and results[alg].get('success', False):
                num_colors = results[alg].get('num_colors', None)
                if num_colors is not None:
                    if min_colors is None or num_colors < min_colors:
                        min_colors = num_colors
        
        # If no algorithm succeeded, use a reasonable estimate
        if min_colors is None:
            max_degree = max(graph.degree(v) for v in range(graph.n)) if graph.n > 0 else 0
            k_for_annealing = max_degree + 1
        else:
            k_for_annealing = min_colors
    
    # Run simulated annealing with the determined k
    try:
        sa_result = simulated_annealing(graph, k=k_for_annealing, max_iter=10000)
        results['annealing'] = {
            'coloring': sa_result.coloring,
            'num_colors': sa_result.num_colors,
            'conflicts': sa_result.conflicts,
            'time': sa_result.time_seconds,
            'success': sa_result.coloring is not None,
            'k_used': k_for_annealing
        }
    except Exception as e:
        results['annealing'] = {'error': str(e), 'success': False}
    
    return results


def experiment_graph_types(n: int, trials: int = 5) -> Dict:
    """
    Compare all algorithms on different graph structures.
    
    This function tests all four algorithms on cycle, complete, path, star,
    bipartite, and random graphs, and returns the results for comparison.
    """
    graph_types = {
        'cycle': cycle_graph(n),
        'complete': complete_graph(n),
        'path': path_graph(n),
        'star': star_graph(n),
        'bipartite': bipartite_graph(n // 2, n - n // 2, p=0.8),
    }
    
    results = {}
    
    # Test each graph type
    for graph_name, graph in graph_types.items():
        print(f"Testing {graph_name} graph (n={n})...")
        result = compare_all_algorithms(graph)
        results[graph_name] = result
    
    # Test random graphs
    print(f"Testing random graphs (n={n}, trials={trials})...")
    random_results = []
    for _ in range(trials):
        random_g = random_graph(n, p=0.3)
        random_results.append(compare_all_algorithms(random_g))
    
    # Average the random graph results
    results['random'] = average_results(random_results)
    
    return results


def average_results(result_list: List[Dict]) -> Dict:
    """
    Average results from multiple runs.
    
    This function takes a list of result dictionaries (from compare_all_algorithms)
    and computes average values for colors used, runtime, and success rate.
    """
    if not result_list:
        return {}
    
    algorithms = ['backtracking', 'greedy', 'dsatur', 'annealing']
    averaged = {}
    
    for alg in algorithms:
        if alg not in result_list[0]:
            continue
        
        # Collect all results for this algorithm
        colors = []
        times = []
        successes = 0
        
        for result in result_list:
            if alg in result and result[alg].get('success', False):
                colors.append(result[alg].get('num_colors', 0))
                times.append(result[alg].get('time', 0))
                successes += 1
        
        if successes > 0:
            averaged[alg] = {
                'avg_colors': sum(colors) / len(colors) if colors else 0,
                'avg_time': sum(times) / len(times) if times else 0,
                'success_rate': successes / len(result_list)
            }
        else:
            averaged[alg] = {'success_rate': 0}
    
    return averaged


def experiment_scalability(max_n: int = 50, step: int = 5) -> Dict:
    """
    Test how algorithms scale with graph size on different graph types.
    
    This function tests algorithms on graphs of increasing size to see how
    their runtime scales. Tests cycle, path, star, and random graphs.
    """
    ns = list(range(step, max_n + 1, step))
    graph_types = ['cycle', 'path', 'star', 'random']
    
    results = {gtype: {'n': [], 'backtracking': [], 'greedy': [], 'dsatur': [], 'annealing': []}
               for gtype in graph_types}
    
    for n in ns:
        print(f"Testing scalability at n={n}...")
        
        # Test each graph type
        if 'cycle' in graph_types:
            g = cycle_graph(n)
            r = compare_all_algorithms(g)
            results['cycle']['n'].append(n)
            results['cycle']['backtracking'].append(r.get('backtracking', {}).get('time', 0))
            results['cycle']['greedy'].append(r.get('greedy', {}).get('time', 0))
            results['cycle']['dsatur'].append(r.get('dsatur', {}).get('time', 0))
            results['cycle']['annealing'].append(r.get('annealing', {}).get('time', 0))
        
        if 'path' in graph_types:
            g = path_graph(n)
            r = compare_all_algorithms(g)
            results['path']['n'].append(n)
            results['path']['backtracking'].append(r.get('backtracking', {}).get('time', 0))
            results['path']['greedy'].append(r.get('greedy', {}).get('time', 0))
            results['path']['dsatur'].append(r.get('dsatur', {}).get('time', 0))
            results['path']['annealing'].append(r.get('annealing', {}).get('time', 0))
        
        if 'star' in graph_types:
            g = star_graph(n)
            r = compare_all_algorithms(g)
            results['star']['n'].append(n)
            results['star']['backtracking'].append(r.get('backtracking', {}).get('time', 0))
            results['star']['greedy'].append(r.get('greedy', {}).get('time', 0))
            results['star']['dsatur'].append(r.get('dsatur', {}).get('time', 0))
            results['star']['annealing'].append(r.get('annealing', {}).get('time', 0))
        
        if 'random' in graph_types:
            # Average over a few random graphs
            random_times = {'backtracking': [], 'greedy': [], 'dsatur': [], 'annealing': []}
            for _ in range(3):
                g = random_graph(n, p=0.3)
                r = compare_all_algorithms(g)
                for alg in random_times:
                    if r.get(alg, {}).get('success', False):
                        random_times[alg].append(r[alg].get('time', 0))
            
            results['random']['n'].append(n)
            for alg in random_times:
                avg_time = sum(random_times[alg]) / len(random_times[alg]) if random_times[alg] else 0
                results['random'][alg].append(avg_time)
    
    return results

