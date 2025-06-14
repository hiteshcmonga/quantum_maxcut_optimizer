import json
import networkx as nx
import os

def load_graph(filepath="data/sample_graph.json") -> nx.Graph:
    """
    Load a graph from a JSON file into a networkx.Graph.
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    full_path = os.path.join(base_path, filepath)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"File not found: {full_path}")

    with open(full_path, 'r') as f:
        data = json.load(f)

    G = nx.Graph()
    for edge in data["edges"]:
        u, v, w = edge["u"], edge["v"], edge.get("weight", 1)
        G.add_edge(u, v, weight=w)

    return G

if __name__ == "__main__":
    graph = load_graph()
    print("Loaded graph with", graph.number_of_nodes(), "nodes and", graph.number_of_edges(), "edges.")