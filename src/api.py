# src/api.py
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from loader import load_graph
from classical import classical_maxcut
from quantum import solve_maxcut_qaoa
from metrics import REQUEST_COUNT, CLASSICAL_TIME, QUANTUM_TIME, BACKEND_USAGE, REGISTRY
import numpy as np

app = FastAPI(title="Quantum Max-Cut API", version="1.0")

@app.get("/")
def root():
    return {"message": "Welcome to the Quantum Max-Cut Optimizer API!"}

@app.get("/solve/classical")
def solve_classical():
    REQUEST_COUNT.labels(endpoint="/solve/classical", method="GET").inc()
    graph = load_graph()
    with CLASSICAL_TIME.time():
        assignment, cut = classical_maxcut(graph)
    return JSONResponse({
        "method": "classical",
        "cut_value": cut,
        "assignment": assignment
    })

@app.get("/solve/quantum")
def solve_quantum():
    REQUEST_COUNT.labels(endpoint="/solve/quantum", method="GET").inc()
    graph = load_graph()
    with QUANTUM_TIME.time():
        bitstring, cut, meta = solve_maxcut_qaoa(graph)
    BACKEND_USAGE.labels(backend=meta["backend"]).inc()
    bitstring_list = [int(b) for b in bitstring]
    cut_value = float(cut)
    meta_clean = {
        k: (int(v) if isinstance(v, np.integer)
            else float(v) if isinstance(v, np.floating)
            else v)
        for k, v in meta.items()
    }
    return JSONResponse({
        "method": "quantum",
        "cut_value": cut_value,
        "bitstring": bitstring_list,
        "metadata": meta_clean
    })

@app.get("/metrics")
def metrics():
    """Prometheus scrape endpoint."""
    data = generate_latest(REGISTRY)
    return Response(data, media_type=CONTENT_TYPE_LATEST)

# Todo: add grafana?
@app.get("/dashboard", response_class=Response)
def dashboard():
    html = """
<!DOCTYPE html>
<html>
<head>
  <title>Max-Cut API Metrics</title>
  <style>
    body { font-family: sans-serif; padding: 2rem; max-width: 600px; margin: auto; }
    h1 { text-align: center; }
    table { border-collapse: collapse; width: 100%; margin-top: 1rem; }
    th, td { padding: 0.5rem; border: 1px solid #ccc; text-align: left; }
    th { background: #f0f0f0; }
    .label { font-weight: bold; }
  </style>
</head>
<body>
  <h1>Max-Cut API Summary</h1>
  <table>
    <tbody id="metrics-body">
      <tr><td colspan="2">Loading…</td></tr>
    </tbody>
  </table>

  <script>
    async function fetchMetrics() {
      const text = await fetch('/metrics').then(r => r.text());
      // split into non-comment lines
      const lines = text.split('\\n').filter(l => l && !l.startsWith('#'));
      // containers for summaries
      const calls = { classical: 0, quantum: 0 };
      const times = { classical: { sum: 0, count: 0 }, quantum: { sum: 0, count: 0 } };
      const backend = {};

      for (const line of lines) {
        const [fullMetric, valStr] = line.split(' ');
        const val = parseFloat(valStr);
        // strip labels => name and labels
        const name = fullMetric.split('{')[0];

        // 1) total calls
        if (name === 'api_requests_total') {
          const endpoint = fullMetric.match(/endpoint="([^"]+)"/)?.[1];
          if (endpoint === '/solve/classical') calls.classical = val;
          if (endpoint === '/solve/quantum')   calls.quantum   = val;
        }

        // 2) collect sum & count for durations
        if (name === 'maxcut_classical_duration_seconds_sum')   times.classical.sum   = val;
        if (name === 'maxcut_classical_duration_seconds_count') times.classical.count = val;
        if (name === 'maxcut_quantum_duration_seconds_sum')     times.quantum.sum     = val;
        if (name === 'maxcut_quantum_duration_seconds_count')   times.quantum.count   = val;

        // 3) backend usage
        if (name === 'quantum_backend_usage_total') {
          const b = fullMetric.match(/backend="([^"]+)"/)?.[1] || 'unknown';
          backend[b] = val;
        }
      }

      // compute averages
      const avgClassical = times.classical.count
        ? (times.classical.sum / times.classical.count).toFixed(3)
        : '—';
      const avgQuantum = times.quantum.count
        ? (times.quantum.sum / times.quantum.count).toFixed(3)
        : '—';

      // build rows
      let rows = `
        <tr><td class="label">Classical calls</td><td>${calls.classical}</td></tr>
        <tr><td class="label">Quantum calls</td><td>${calls.quantum}</td></tr>
        <tr><td class="label">Avg classical solve time (s)</td><td>${avgClassical}</td></tr>
        <tr><td class="label">Avg quantum solve time (s)</td><td>${avgQuantum}</td></tr>
        <tr><th colspan="2">Quantum backend usage</th></tr>
      `;
      for (const [b, count] of Object.entries(backend)) {
        rows += `<tr><td class="label">${b}</td><td>${count}</td></tr>`;
      }

      document.getElementById('metrics-body').innerHTML = rows;
    }

    fetchMetrics();
    setInterval(fetchMetrics, 5000);
  </script>
</body>
</html>
"""
    return Response(html, media_type="text/html")