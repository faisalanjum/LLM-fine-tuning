# GPT2Model + its blocks + GPT-2's HF weight-mapping (load_weights_into_gpt).

import torch
import torch.nn as nn
from reference.activation_fns import GELU


class FeedForward(nn.Module):

    def __init__(self, emb_dim):
        
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(emb_dim, 4 * emb_dim),
            GELU(),
            nn.Linear(4 * emb_dim, emb_dim)
        )
        
    def forward(self, x):
        return self.layers(x)




class LayerNorm(nn.Module):

    def __init__(self,emd_dim):

        super().__init__()
        self.eps   = 1e-5
        self.shift = nn.Parameter(torch.zeros(emd_dim))
        self.scale = nn.Parameter(torch.ones(emd_dim))

    def forward(self, x):
        mean   = x.mean(dim=-1, keepdim=True)
        var    = x.var(dim=-1, keepdim=True, unbiased = False)
        norm_x = (x - mean)/torch.sqrt(var + self.eps)

        return self.shift + self.scale * norm_x


class MaskedMultiHeadAttn(nn.Module):
    
    def __init__(self, d_in, d_out, context_length, drop_rate, n_heads, qkv_bias = False):
        super().__init__()
        assert(d_out % n_heads == 0)

        self.d_in    = d_in
        self.d_out   = d_out
        self.n_heads = n_heads
        self.head_dim = d_out // n_heads
        

        self.W_query  = nn.Linear(d_in, d_out, qkv_bias)
        self.W_key    = nn.Linear(d_in, d_out, qkv_bias)
        self.W_value  = nn. Linear(d_in, d_out, qkv_bias)
        self.out_proj = nn.Linear(d_out, d_out)
        self.dropout  = nn.Dropout(drop_rate)

        self.register_buffer("mask",torch.triu(torch.ones(context_length, context_length), diagonal =1))


    def forward(self, x):
        batch_size, seq_length, emb_dim = x.shape

        # shape: (batch_size, seq_length, d_in) --> (batch_size, seq_length, d_out)
        queries = self.W_query(x)  
        keys    = self.W_key(x)
        values  = self.W_value(x)

        # split d_out into n_heads & head_dim: (batch_size, seq_length, n_heads, head_dim)
        queries = queries.view(batch_size, seq_length, self.n_heads, self.head_dim) 
        keys    = keys.view(batch_size, seq_length, self.n_heads, self.head_dim) 
        values  = values.view(batch_size, seq_length, self.n_heads, self.head_dim) 

        # group by n_heads instead of seq_length: (batch_size, n_heads, seq_length, head_dim)
        queries = queries.transpose(1,2)
        keys    = keys.transpose(1,2)
        values  = values.transpose(1,2)

        # Attn Score: (batch_size, n_heads, seq_length, seq_length)
        attn_scores = queries @ keys.transpose(2,3)

        # Masking
        mask_bool = self.mask.bool()[:seq_length,:seq_length]
        attn_scores.masked_fill_(mask_bool, -torch.inf)

        # Attn Weights: (batch_size, n_heads, seq_length, seq_length) 
        d_k = keys.shape[-1]
        attn_wts = torch.softmax(attn_scores / d_k **0.5, dim = -1)
        attn_wts = self.dropout(attn_wts)

        # context vector: (batch_size, n_heads, seq_length, head_dim)
        context_vecs = attn_wts @ values

        # context vector: (batch_size, seq_length, n_heads, head_dim)
        context_vecs = context_vecs.transpose(1,2)

        # context vector: (batch_size, seq_length, d_out)
        context_vecs = context_vecs.contiguous().view(batch_size, seq_length, self.d_out)

        context_vecs = self.out_proj(context_vecs)
        return context_vecs



class TransformerBlock(nn.Module):

    def __init__(self, cfg):
        super().__init__()

        self.attn = MaskedMultiHeadAttn(
                        d_in  = cfg["emb_dim"],
                        d_out = cfg["emb_dim"],
                        context_length = cfg["context_length"],
                        drop_rate = cfg["drop_rate"],
                        n_heads   = cfg["n_heads"],
                        qkv_bias  = cfg["qkv_bias"])

        self.ff    = FeedForward(cfg["emb_dim"])
        self.norm1 = LayerNorm(cfg["emb_dim"])
        self.norm2 = LayerNorm(cfg["emb_dim"])
        self.drop_shortcut    = nn.Dropout(cfg["drop_rate"])

    
    def forward(self,x):

        shortcut = x
        x = self.norm1(x)
        x = self.attn(x)
        x = self.drop_shortcut(x)
        x = x + shortcut

        shortcut = x
        x = self.norm2(x)
        x = self.ff(x)
        x = self.drop_shortcut(x)
        x = x + shortcut

        return x


class GPT2Model(nn.Module):

    def __init__(self, cfg):
        super().__init__()

        self.tok_emb  = nn.Embedding(cfg['vocab_size'], cfg['emb_dim'])
        self.pos_emb  = nn.Embedding(cfg['context_length'], cfg['emb_dim'])
        self.drop_emb = nn.Dropout(cfg['drop_rate']) 

        self.trf_blocks = nn.Sequential(
            *[TransformerBlock(cfg) for _ in range(cfg['n_layers'])])

        self.final_norm = LayerNorm(cfg["emb_dim"])

        # nn.Linear always operates on the last dimension—this is built into its design. So you don’t need to specify dim=-1
        # [2, 4, emb_dim] → [2, 4, vocab_size]
        self.out_head = nn.Linear(cfg['emb_dim'],cfg['vocab_size'], bias = False)


    def forward(self, in_idx):
        
        batch_size, seq_len = in_idx.shape
        tok_embeds = self.tok_emb(in_idx)
        pos_embeds = self.pos_emb(
            torch.arange(seq_len, device = in_idx.device)
        )
        
        x = tok_embeds + pos_embeds

        x = self.drop_emb(x)
        x = self.trf_blocks(x)
        x = self.final_norm(x)
        logits = self.out_head(x)

        return logits


def load_weights_into_gpt(model, w):
    
    def assign(slot, numbers):  # copies, refuses wrong shapes, remembers what's filled
        assert slot.shape == numbers.shape, f"{list(slot.shape)} vs {list(numbers.shape)}"
        with torch.no_grad():
            slot.copy_(numbers)

    assign(model.tok_emb.weight, w["wte.weight"])
    assign(model.pos_emb.weight, w["wpe.weight"])
    
    for i, b in enumerate(model.trf_blocks):
        h = f"h.{i}."
        q, k, v = w[h + "attn.c_attn.weight"].chunk(3, dim=-1)
        assign(b.attn.W_query.weight, q.T); assign(b.attn.W_key.weight, k.T); assign(b.attn.W_value.weight, v.T)
        q, k, v = w[h + "attn.c_attn.bias"].chunk(3, dim=-1)
        assign(b.attn.W_query.bias, q); assign(b.attn.W_key.bias, k); assign(b.attn.W_value.bias, v)
        assign(b.attn.out_proj.weight, w[h + "attn.c_proj.weight"].T)
        assign(b.attn.out_proj.bias, w[h + "attn.c_proj.bias"])
        assign(b.ff.layers[0].weight, w[h + "mlp.c_fc.weight"].T)
        assign(b.ff.layers[0].bias, w[h + "mlp.c_fc.bias"])
        assign(b.ff.layers[2].weight, w[h + "mlp.c_proj.weight"].T)
        assign(b.ff.layers[2].bias, w[h + "mlp.c_proj.bias"])
        assign(b.norm1.scale, w[h + "ln_1.weight"]); assign(b.norm1.shift, w[h + "ln_1.bias"])
        assign(b.norm2.scale, w[h + "ln_2.weight"]); assign(b.norm2.shift, w[h + "ln_2.bias"])
    assign(model.final_norm.scale, w["ln_f.weight"])
    assign(model.final_norm.shift, w["ln_f.bias"])
    assign(model.out_head.weight, w["wte.weight"])  # reuse: GPT-2 has no separate output layer
    

