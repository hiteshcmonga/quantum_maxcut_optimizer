# src/api.py
from fastapi import FastAPI
from pydantic import BaseModel
from loader import load_graph
from classical import classical_maxcut
from quantum import solve_maxcut_qaoa
from typing import List

app = FastAPI(title="Hybrid Max-Cut API")

class MaxCutResponse(BaseModel):
    classical_cut: int
    quantum_cut: float
    quantum_bits: List[int]
    metadata: dict

@app.get("/maxcut", response_model=MaxCutResponse)
def run_maxcut():
    graph = load_graph("data/sample_graph.json")
    # Classical result
    _, classical_cut = classical_maxcut(graph)
    # Quantum result
    bits, quantum_cut, metadata = solve_maxcut_qaoa(graph, p=1)

    return MaxCutResponse(
        classical_cut=classical_cut,
        quantum_cut=quantum_cut,
        quantum_bits=bits,
        metadata=metadata
    )