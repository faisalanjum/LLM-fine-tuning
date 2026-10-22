# Dataset classes, collate_fn, and the create_dataloader / loader builders.

import json
import requests
from pathlib import Path

def load_instruction_data():
    path = Path(__file__).resolve().parent.parent / "data/downloads/instruction-data.json"

    # Download and save only if the file is missing.
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        url = "https://raw.githubusercontent.com/rasbt/LLMs-from-scratch/main/ch07/01_main-chapter-code/instruction-data.json"
        response = requests.get(url)
        response.raise_for_status()
        path.write_text(response.text, encoding="utf-8")

    return json.loads(path.read_text(encoding="utf-8"))




def load_pretraining_data(
    file_name="the-verdict.txt",
    url="https://raw.githubusercontent.com/rasbt/LLMs-from-scratch/main/ch02/01_main-chapter-code/the-verdict.txt",
):
    path = Path(__file__).resolve().parent.parent / "data/downloads" / file_name

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        path.write_bytes(response.content)

    return path.read_text(encoding="utf-8")