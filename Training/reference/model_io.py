# the model's inputs/outputs + checkpoint I/O: text_to_token_ids, token_ids_to_text, save_checkpoint, load_checkpoint (and later a load_model helper)




# Check LoadWeights.ipynb for more details.
def download_weights(repo="openai-community/gpt2"):
    
    from glob import glob
    from huggingface_hub import snapshot_download
    from safetensors.torch import load_file
    
    path = snapshot_download(repo, allow_patterns=["model*.safetensors", "config.json"])
    w = {}
    for f in glob(f"{path}/model*.safetensors"):
        w.update(load_file(f))
    return w


# [1, N] = one example with N tokens.
# Text (str) → token-ID tensor [1, N], e.g. tensor([[10, 20, 30]]).
def text_to_token_ids(text, tokenizer):
  import torch
  encoded = tokenizer.encode(text, allowed_special={'<|endoftext|>'})
  encoded_tensor = torch.tensor(encoded).unsqueeze(0)
  return encoded_tensor

# Token-ID tensor [1, N] → text (str).
def token_ids_to_text(token_ids, tokenizer):
  flat = token_ids.squeeze(0)
  return tokenizer.decode(flat.tolist())
