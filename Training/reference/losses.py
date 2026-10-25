# objectives: calc_loss_batch, calc_loss_loader now; instruction/DPO/GRPO
import torch

def calc_loss_batch(input_batch, target_batch, model, device):
    input_batch  = input_batch.to(device)
    target_batch = target_batch.to(device)
    logits = model(input_batch)
    loss = torch.nn.functional.cross_entropy(
        logits.flatten(0,1), target_batch.flatten())

    return loss

# Override Pretraining loss since now we are only concerned with final Output
def calc_loss_batch_classification(input_batch, target_batch, model, device):
    input_batch  = input_batch.to(device)
    target_batch = target_batch.to(device)

    logits = model(input_batch)[:,-1,:]
    loss = torch.nn.functional.cross_entropy(logits, target_batch)
    return loss

def calc_loss_loader(data_loader, model, device, loss_fn=calc_loss_batch, num_batches=None):

    total_loss = 0.0

    if len(data_loader) == 0:
        return float("nan")
    elif num_batches is not None:
        num_batches = min(num_batches, len(data_loader))
    else:
        num_batches = len(data_loader)

    for i, (input_batch, target_batch) in enumerate(data_loader):
        if i < num_batches:
            loss = loss_fn(input_batch, target_batch, model, device)
            total_loss += loss.item()
        else:
            break

    return total_loss/ num_batches
