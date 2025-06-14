# src/qdo/compare.py

import matplotlib.pyplot as plt
import networkx as nx

from loader import load_graph
from classical import classical_maxcut, get_classical_colors
from quantum import solve_maxcut_qaoa, get_quantum_colors

def compare_and_visualize():
    print("\nLoading graph...")
    graph = load_graph()

    print("\nSolving classically...")
    classical_assignment, classical_cut = classical_maxcut(graph)

    print("\nSolving with QAOA (Quantum)...")
    quantum_bits, quantum_cut, metadata = solve_maxcut_qaoa(graph, p=1)

    print("\nSummary:")
    print(f"Classical Cut Value: {classical_cut}")
    print(f"Quantum Cut Value:   {quantum_cut}")
    print(f"Quantum Metadata:    {metadata}")

    # Compare cut values
    plt.figure(figsize=(6, 4))
    plt.bar(["Classical", "Quantum"], [classical_cut, quantum_cut], color=["skyblue", "salmon"])
    plt.ylabel("Cut Value")
    plt.title("Max-Cut: Classical vs Quantum")
    plt.tight_layout()
    plt.show()

    # Compare partitioning visually
    pos = nx.spring_layout(graph, seed=42)

    classical_nodes, classical_edges = get_classical_colors(graph, classical_assignment)
    quantum_nodes, quantum_edges = get_quantum_colors(graph, quantum_bits)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    nx.draw(graph, pos, node_color=classical_nodes, edge_color=classical_edges, with_labels=True,
            ax=axes[0], node_size=600)
    axes[0].set_title("Classical Max-Cut")

    nx.draw(graph, pos, node_color=quantum_nodes, edge_color=quantum_edges, with_labels=True,
            ax=axes[1], node_size=600)
    axes[1].set_title("Quantum Max-Cut (QAOA)")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    compare_and_visualize()