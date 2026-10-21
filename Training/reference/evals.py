#  metrics (accuracy, perplexity) and, when needed, the optional Qwen judge.

import requests

BASE = "http://localhost:11434"

def query_model(prompt, model, think=None):
    """Send a prompt to any local model and return its reply.

    think=False hides reasoning on reasoning models (e.g. qwen3);
    leave it as None for models that don't support thinking.
    """
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    if think is not None:
        payload["think"] = think
    r = requests.post(f"{BASE}/api/chat", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["message"]["content"]