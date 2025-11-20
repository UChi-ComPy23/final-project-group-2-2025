import random
from typing import List, Tuple

import matplotlib.pyplot as plt
import networkx as nx


from src.graph import Graph, is_proper_coloring
from src.backtracking import backtracking_coloring, BacktrackingResult


def erdos_renyi_graph(n: int, p: float, seed: int | None = None) -> Graph:
    """
    Generate an undirected Erdős-Rényi G(n, p) graph
    using our Graph class.
    """
    rng = random.Random(seed)
    g = Graph(n)
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                g.add_edge(u, v)
    return g


def graph_to_networkx(graph: Graph) -> nx.Graph:
    """
    Convert our Graph class to a NetworkX Graph for visualization.
    """
    G_nx = nx.Graph()
    G_nx.add_nodes_from(range(graph.n))
    for u in range(graph.n):
        for v in graph.adj[u]:
            if u < v:
                G_nx.add_edge(u, v)
    return G_nx


def draw_coloring(
    graph: Graph,
    coloring: List[int],
    filename: str,
    title: str | None = None,
    layout_seed: int = 0,
) -> None:
    """
    Draw a colored graph using NetworkX and save it as an image.
    """
    G_nx = graph_to_networkx(graph)

    # Number of colors used
    k = max(coloring) + 1 if coloring else 0

    # Use a qualitative colormap; tab10 has 10 distinct colors
    cmap = plt.get_cmap("tab10")
    node_colors = [cmap(c % 10) for c in coloring]

    # Layout: spring layout with fixed seed for reproducibility
    pos = nx.spring_layout(G_nx, seed=layout_seed)

    plt.figure(figsize=(5, 5))
    nx.draw_networkx(
        G_nx,
        pos=pos,
        node_color=node_colors,
        with_labels=True,
        node_size=500,
        font_size=10,
    )
    if title:
        plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


def run_backtracking_example(n: int, p: float, seed: int, filename: str) -> None:
    """
    Generate a random G(n, p) graph, run backtracking coloring,
    and save a figure with the optimal coloring.
    """
    print(f"Running backtracking example: n={n}, p={p}, seed={seed}")

    graph = erdos_renyi_graph(n=n, p=p, seed=seed)
    result: BacktrackingResult = backtracking_coloring(graph, use_degree_order=True)

    print(result)

    if result.coloring is None or result.num_colors < 0:
        print("Backtracking failed to find a coloring (this should be rare).")
        return

    # Sanity check: the result should be a proper coloring
    assert is_proper_coloring(graph, result.coloring), "Coloring is not proper!"

    title = (
        f"Backtracking optimal coloring\n"
        f"n={n}, p={p}, k={result.num_colors}"
    )

    draw_coloring(
        graph=graph,
        coloring=result.coloring,
        filename=filename,
        title=title,
        layout_seed=0,
    )

    print(f"Saved figure to {filename}\n")


def main() -> None:
    """
    Generate the example figures used in the report.
    """
    p = 0.3

    # Example 1: n=10 -> BT_graph1.png
    run_backtracking_example(
        n=10,
        p=p,
        seed=42,
        filename="BT_graph1.png",
    )

    # Example 2: n=14 -> BT_graph2.png
    run_backtracking_example(
        n=14,
        p=p,
        seed=123,
        filename="BT_graph2.png",
    )


if __name__ == "__main__":
    main()
