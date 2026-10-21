# train_model_simple, evaluate_model, print_progress

import torch
from reference.losses import calc_loss_batch, calc_loss_loader
from reference.generate import generate_and_print_sample


def evaluate_model(model, train_loader, val_loader, device, eval_iter):

    model.eval()
    with torch.no_grad():
        train_loss = calc_loss_loader(train_loader, model, device, num_batches=eval_iter)
        val_loss   = calc_loss_loader(val_loader, model, device, num_batches=eval_iter)

    model.train()
    return train_loss, val_loss
    

def train_model_simple(model, optimizer, device, tokenizer,
                       train_loader, val_loader,
                       eval_freq, eval_iter,
                       start_context, num_epoch):

    train_losses, val_losses, track_tokens_seen = [], [], []
    tokens_seen, global_step = 0, -1

    for epoch in range(num_epoch):
        model.train()
        for input_batch, target_batch in train_loader:

            # Usual training steps
            optimizer.zero_grad()
            loss = calc_loss_batch(input_batch, target_batch, model=model, device=device)
            loss.backward()
            optimizer.step()

            tokens_seen += input_batch.numel()
            global_step += 1

            if global_step % eval_freq == 0:
                train_loss, val_loss = evaluate_model(model, train_loader, val_loader, device, eval_iter)

                train_losses.append(train_loss)
                val_losses.append(val_loss)
                track_tokens_seen.append(tokens_seen)

                print(f"epoch:{epoch+1}, step:{global_step:06d}: "
                      f"train_loss:{train_loss:.3f}, "
                      f"val_loss:{val_loss:.3f}"
                )
        

        generate_and_print_sample(model, tokenizer, device, start_context)

    return train_losses, val_losses, track_tokens_seen
