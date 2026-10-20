# REFERENCE ONLY — do not run this file.
# This is a copy-paste template for the §6 "Save" cell of a notebook (e.g. 03_instruction.ipynb).
# Paste it into that cell, uncomment, and fill in the ... values.
#
# import json, os, torch
#
# run_dir = "runs/instruction/001_baseline"
# os.makedirs(run_dir, exist_ok=True)
#
# # config.json — what you ran
# json.dump({"model": ..., "seed": ..., "lr": ..., "epochs": ..., "batch_size": ...},
#           open(f"{run_dir}/config.json", "w"), indent=2)
#
# # predictions.jsonl — one {prompt, answer} per line
# with open(f"{run_dir}/predictions.jsonl", "w") as f:
#     for prompt, answer in results:          # your generated answers
#         f.write(json.dumps({"prompt": prompt, "answer": answer}) + "\n")
#
# # metrics.json — your scores
# json.dump({"accuracy": ...}, open(f"{run_dir}/metrics.json", "w"), indent=2)
#
# # model.pth — optional checkpoint
# torch.save(model.state_dict(), f"{run_dir}/model.pth")
