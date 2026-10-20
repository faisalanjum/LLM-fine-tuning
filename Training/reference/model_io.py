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
