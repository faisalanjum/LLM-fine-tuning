# How §6 saves a run. Pseudocode — commented out; uncomment and fill in when training.
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
