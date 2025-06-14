# src/qdo/quantum.py

import networkx as nx
import numpy as np
from typing import Tuple, List

from qiskit.primitives import Sampler
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.translators import from_docplex_mp
from qiskit_optimization.converters import QuadraticProgramToQubo
from docplex.mp.model import Model

def create_maxcut_qubo(graph: nx.Graph) -> QuadraticProgram:
    mdl = Model(name="MaxCut")
    x = [mdl.binary_var(name=f"x_{i}") for i in range(graph.number_of_nodes())]
    obj = mdl.sum(graph[i][j].get("weight", 1) * (x[i] + x[j] - 2 * x[i] * x[j])
                  for i, j in graph.edges())
    mdl.maximize(obj)
    return from_docplex_mp(mdl)

def solve_maxcut_qaoa(graph: nx.Graph, p: int = 1) -> Tuple[List[int], float, dict]:
    qp = create_maxcut_qubo(graph)
    qubo = QuadraticProgramToQubo().convert(qp)

    qaoa = QAOA(sampler=Sampler(), optimizer=COBYLA(), reps=p)
    result = MinimumEigenOptimizer(qaoa).solve(qubo)

    bitstring = result.x
    cost = -result.fval
    metadata = {
        "num_qubits": qp.get_num_binary_vars(),
        "circuit_depth": qaoa.ansatz.depth(),
        "backend": "Sampler"
    }
    return bitstring, cost, metadata

def get_quantum_colors(graph: nx.Graph, bitstring: List[int]):
    node_colors = ['skyblue' if bit == 0 else 'salmon' for bit in bitstring]
    edge_colors = ['green' if bitstring[u] != bitstring[v] else 'gray' for u, v in graph.edges]
    return node_colors, edge_colors