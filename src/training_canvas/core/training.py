# --- Training Script for sketch data
import torch.cuda
from torch import optim
from torch.optim.lr_scheduler import StepLR
from torch.utils.data import DataLoader, random_split
from torchvision.transforms import transforms
import torch.nn.functional as F

from training_canvas.core.dataset import SketchDataset
from training_canvas.core.models import Net

# jus: left off here
CUDA_LAUNCH_BLOCKING = 1

def train(model: torch.nn.Module, device, loss_fn, optimizer, epoch: int, train_dataloader, log_interval = 100, dry_run=False):
    model.train()
    for batch, (image, label) in enumerate(train_dataloader):
        image, label = image.to(device), label.to(device)
        optimizer.zero_grad()
        output = model(image)
        loss = loss_fn(output, label)
        loss.backward()
        optimizer.step()
        if batch % log_interval == 0:
            print(f"Train Epoch: {epoch=}, {batch*len(image)=}, {len(train_dataloader)=}, Loss: {loss.item()}")

            if dry_run:
                break

def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


if __name__ == '__main__':
    # Cuda
    # device = ('cuda' if torch.cuda.is_available() else 'cpu')
    device = 'cpu'

    # Dataset and DataLoader
    transform = torch.nn.Sequential(
        transforms.Resize((28, 28)),
        # transforms.Normalize((0.1307,), (0.3081,)),  # TODO: investigate what to do about normalization
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.ConvertImageDtype(torch.float32)
    )
    dataset = SketchDataset(transform=transform)
    train_dataset, validation_dataset = random_split(dataset, [0.75, 0.25], generator=torch.Generator().manual_seed(99))
    train_dataloader = DataLoader(train_dataset)
    validation_dataloader = DataLoader(validation_dataset)

    model = Net().to(device)
    optimizer = optim.Adadelta(model.parameters(), lr=0.01)
    scheduler = StepLR(optimizer, step_size=1, gamma=0.1)
    loss = torch.nn.NLLLoss()
    for epoch in range(1, 101):
        train(model=model, device=device, loss_fn=loss, optimizer=optimizer, epoch=epoch, train_dataloader=train_dataloader,dry_run=True)
