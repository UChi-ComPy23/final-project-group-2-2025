import random
from src.graph import Graph
import networkx as nx
import matplotlib.pyplot as plt


def random_graph(n, p):
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                edges.append((u, v))
    return Graph.from_edge_list(n, edges)

def plot_colored_graph(graph, colors, title="Colored Graph"):
    # Build NetworkX graph
    G = nx.Graph()
    G.add_nodes_from(range(graph.n))
    for u in range(graph.n):
        for v in graph.adj[u]:
            if u < v:
                G.add_edge(u, v)
    
    # Choose a layout
    pos = nx.spring_layout(G, seed=42)
    
    # Draw nodes with colors
    nx.draw(
        G, pos,
        node_color=colors,
        with_labels=True,
        cmap=plt.cm.Set3,
        node_size=400,
        edge_color="gray"
    )
    
    plt.title(title)
    plt.show()