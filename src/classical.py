# src/qdo/classical.py

import networkx as nx
import random
from typing import Tuple, Dict

def classical_maxcut(graph: nx.Graph) -> Tuple[Dict[int, int], int]:
    """
    Solves the Max-Cut problem using a random approach: split nodes into two groups at random and count edges
    that connect nodes in different groups (i.e., the cut).
    """
    assignment = {node: random.randint(0, 1) for node in graph.nodes}
    cut_value = sum(1 for u, v in graph.edges if assignment[u] != assignment[v])
    return assignment, cut_value

def get_classical_colors(graph: nx.Graph, assignment: Dict[int, int]):
    # Assign colors to nodes by group and edges by whether they cross the cut
    node_colors = ['skyblue' if assignment[n] == 0 else 'salmon' for n in graph.nodes]
    edge_colors = ['green' if assignment[u] != assignment[v] else 'gray' for u, v in graph.edges]
    return node_colors, edge_colors
