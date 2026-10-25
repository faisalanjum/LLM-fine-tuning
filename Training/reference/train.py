# train_model_simple, evaluate_model, print_progress

import torch
from reference.losses import calc_loss_batch, calc_loss_loader, calc_loss_batch_classification
from reference.generate import generate_and_print_sample
from reference.evals import calc_accuracy_loader

def evaluate_model(model, train_loader, val_loader, device, eval_iter, loss_fn=calc_loss_batch):

    model.eval()
    with torch.no_grad():
        train_loss = calc_loss_loader(train_loader, model, device, loss_fn=loss_fn, num_batches=eval_iter)
        val_loss   = calc_loss_loader(val_loader, model, device, loss_fn=loss_fn, num_batches=eval_iter)

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


def train_classifier_simple(model, device, tokenizer, optimizer,
                            train_loader, val_loader,
                            eval_freq, eval_iter,
                            epochs):
    
    train_losses, val_losses, train_accs, val_accs = [], [], [], []
    global_step, examples_seen = -1, 0
    
    for epoch in range(epochs):
        model.train()
        for i,(input_batch, target_batch) in enumerate(train_loader):
            optimizer.zero_grad()
            loss = calc_loss_batch_classification(input_batch, target_batch, model, device)
            loss.backward()
            optimizer.step()
            
            global_step += 1
            examples_seen += input_batch.shape[0]

            if global_step % eval_freq == 0:
                train_loss, val_loss = evaluate_model(model, train_loader, val_loader, device, 
                                                    eval_iter=eval_iter, loss_fn=calc_loss_batch_classification)
                train_losses.append(train_loss)
                val_losses.append(val_loss)

                print(f"epoch:{epoch+1}, step:{global_step:06d}: "
                      f"Train loss:{train_loss:.3f}, "
                      f"Val loss:{val_loss:.3f}"
                )  

        train_accuracy = calc_accuracy_loader(train_loader, model, device, num_batches = eval_iter)
        val_accuracy   = calc_accuracy_loader(val_loader, model, device, num_batches = eval_iter)
        train_accs.append(train_accuracy)
        val_accs.append(val_accuracy)

        print(f"Training accuracy: {train_accuracy*100:.2f}% | ", end="")
        print(f"Validation accuracy: {val_accuracy*100:.2f}%")
    
    return train_losses, val_losses, train_accs, val_accs, examples_seen
