# Example run — instruction / 001_baseline

Template for one saved training run. (This folder is gitignored — local only.)

```
runs/instruction/001_baseline/
├── config.json        # what you ran: model, seed, lr, epochs, batch_size
├── predictions.jsonl  # the model's answers on the test prompts (one JSON per line)
├── metrics.json       # scores, e.g. {"accuracy": ...}
└── model.pth          # optional checkpoint (weights), written by torch.save
```

See `save_run.py` for how these files get written. Next experiment → new folder `002_<name>/`.
