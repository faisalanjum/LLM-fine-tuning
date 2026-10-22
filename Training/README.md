# Training — practice hub

Run notebooks from `Training/`.

## Files

| File | Status |
|---|---|
| [`00_template.ipynb`](00_template.ipynb) | copy to start a new job |
| [`01_pretraining.ipynb`](01_pretraining.ipynb) | in progress |
| [`02_classification.ipynb`](02_classification.ipynb) | skeleton |
| [`02_classification_lora.ipynb`](02_classification_lora.ipynb) | classification with LoRA; skeleton |
| [`03_instruction.ipynb`](03_instruction.ipynb) | in progress |
| [`reference/`](reference/) | shared implementations |

## The three methods

| Method | Data | Loss | Metric |
|---|---|---|---|
| Pretraining | text | next-token CE | perplexity |
| Classification | input + label | CE on class scores (last non-padding token) | accuracy |
| Instruction | prompt + response | next-token CE (prompt tokens currently count) | response quality |

Practice/extraction cycle: write a component in the notebook, understand its tiny example, move it to `reference/`, then later rewrite it from scratch while reusing the rest.
