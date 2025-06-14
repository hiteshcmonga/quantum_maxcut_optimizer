# Hybrid Max-Cut solver
A hybrid classical–quantum solver for the Max-Cut problem.
Key features:
- Quantum Approximate Optimization Algorithm (QAOA) via Qiskit
- Classical randomized baseline for Max-Cut
- Modular architecture suitable for API deployment and CI pipelines
- Metric and visualization-based comparison

---

## Background

The Max-Cut problem aims to partition the nodes of a graph into two sets such that the number (or weight) of edges between the sets is maximized.

This project provides:
- A classical approximation using randomized greedy partitioning
- A quantum-based solution using QAOA
- Comparative analysis via visualizations and numerical metrics
- A codebase organized for scalability into web apps, APIs, and cloud platforms

## Screenshot & Demo


## Planned enhancements:
- [ ] FastAPI interface for graph upload and remote solving
- [ ] CI/CD pipeline with GitHub Actions, Pytest, Linting
- [ ] Streamlit dashboard for interactive result browsing
- [ ] IBMQ backend integration for live quantum execution
- [ ] Graph library for benchmarking performance across inputs

## References
- Qiskit QAOA Documentation: https://qiskit.org/documentation/stubs/qiskit.algorithms.QAOA.html
- Qiskit Optimization Tutorials: https://qiskit.org/documentation/optimization/
- Max-Cut Problem Overview: https://en.wikipedia.org/wiki/Maximum_cut
- Max-Cut using QAOA (PyQuil): https://qiskit-rigetti.readthedocs.io/en/v0.4.1/examples/qaoa_pyquil.html
