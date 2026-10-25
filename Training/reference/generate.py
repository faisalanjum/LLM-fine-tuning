# decoding/sampling: generate, generate_and_print_sample.
import torch
from reference.model_io import text_to_token_ids, token_ids_to_text

def generate(model, idx, max_new_tokens, context_length,
                      temperature = 0.0, top_k = None,  eos_id = None):

  for i in range(max_new_tokens):
    idx_cond = idx[:, -context_length:]
    with torch.no_grad():
     logits = model(idx_cond)

    logits = logits[:,-1,:]

    if top_k is not None:
      topk_values, _ = torch.topk(logits, top_k)
      min_val = topk_values[:,-1:]
      logits = torch.where(
          condition = logits < min_val,
          input = torch.tensor(float("-inf")).to(logits.device),
          other = logits)

    if temperature > 0.0:
      logits = logits/temperature
      probs = torch.softmax(logits, dim = -1)
      idx_next = torch.multinomial(probs, num_samples = 1)

    else:
      idx_next = torch.argmax(logits, dim = -1, keepdim = True)

    if idx_next == eos_id:
      break

    idx = torch.cat((idx, idx_next), dim = 1)

  return idx


def generate_text_simple(model, idx, max_new_tokens, context_size):
  
    for _ in range(max_new_tokens):
        idx_cond = idx[:,-context_size:]

        with torch.no_grad():
            logits = model(idx_cond)
        
        logits   = logits[:, -1, :]
        probas   = torch.softmax(logits, dim = -1)
        idx_next = torch.argmax(probas, dim=-1, keepdim=True)
        idx      = torch.cat((idx, idx_next), dim = 1) 

    return idx


def generate_and_print_sample(model, tokenizer, device, start_context):
  
    model.eval()
    context_size = model.pos_emb.weight.shape[0]
    encoded = text_to_token_ids(start_context, tokenizer).to(device)
  
    with torch.no_grad():
        generated_ids = generate_text_simple(
            model = model, 
            idx = encoded, 
            max_new_tokens = 50, 
            context_size = context_size)
    
    decoded_text = token_ids_to_text(generated_ids, tokenizer)
    print(decoded_text.replace("\n", " "))
    model.train()


def classify_review(txt, model, tokenizer, device, max_length=None):

    model.eval()
    
    encoded_txt = tokenizer.encode(txt)
    model_context_length = model.pos_emb.weight.shape[0]
    pad_token_id = tokenizer.eot_token
    
    if max_length is not None:
        max_length = min(max_length, model_context_length)
    else:
        max_length = model_context_length
    
    encoded_txt = encoded_txt[:max_length]
    encoded_txt += [pad_token_id]*(max_length - len(encoded_txt))

    encoded_tensor = torch.tensor(encoded_txt).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(encoded_tensor)[:,-1,:]
    predicted_label = torch.argmax(logits, dim =-1).item()

    return "spam" if predicted_label == 1 else "not spam"
