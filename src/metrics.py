# src/metrics.py
from prometheus_client import Counter, Histogram, CollectorRegistry

# Create a standalone registry so default collectors aren't auto-registered
REGISTRY = CollectorRegistry(auto_describe=False)

# Total requests received by the API
REQUEST_COUNT = Counter(
    "api_requests_total", 
    "Total number of API requests received", 
    ["endpoint", "method"],
    registry=REGISTRY,
)

# Time spent solving Max-Cut classically
CLASSICAL_TIME = Histogram(
    "maxcut_classical_duration_seconds", 
    "Execution time for classical Max-Cut solver",
    registry=REGISTRY,
)

# Time spent solving Max-Cut using QAOA
QUANTUM_TIME = Histogram(
    "maxcut_quantum_duration_seconds", 
    "Execution time for quantum Max-Cut solver",
    registry=REGISTRY,
)

# Track number of times each backend is used
BACKEND_USAGE = Counter(
    "quantum_backend_usage_total", 
    "Counts how often each quantum backend is used", 
    ["backend"],
    registry=REGISTRY,
)