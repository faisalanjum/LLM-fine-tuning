#  metrics (accuracy, perplexity) and, when needed, the optional Qwen judge.

import requests
import torch

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


def calc_accuracy_loader(data_loader, model, device, num_batches = None):
    model.eval()

    if num_batches is None:
        num_batches = len(data_loader)        
    else:
        num_batches = min(num_batches, len(data_loader))

    correct_prediction = 0
    num_examples    = 0

    for i, (input_batch, label_batch) in enumerate(data_loader):
        if i < num_batches:
            input_batch = input_batch.to(device)
            label_batch = label_batch.to(device)
            
            with torch.no_grad():
                logits  = model(input_batch)[:,-1,:]
            predictions = torch.argmax(logits, dim = -1)

            num_examples         += input_batch.shape[0]
            correct_prediction   += ((label_batch == predictions).sum().item())

        else:
            break
    
    return correct_prediction/num_examples