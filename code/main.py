import os
import numpy as np
from geopy import distance
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from datetime import datetime
from stack_image import StackedImageDataset
from model import StreetViewNet
from args import args

data_path = '../data/640x640/'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device {device}")

writer = SummaryWriter()

transform = transforms.Compose([
    transforms.Resize((160, 160)),
    transforms.ToTensor(),

    # Because I am not sure that it will affect StackedImageDataset, so I won't touch it.
    # I think that these 2 lines will affect very much
    # adding flipping, affine pictures into dataset
    # transforms.RandomHorizontalFlip(),
    # transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.8, 1.2)),
    
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])   
])

dataset = StackedImageDataset(data_path, transform=transform)
train_size = int((1 - args.val_ratio) * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

model = StreetViewNet().to(device)
model.train()
loss_fn = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

if __name__ == '__main__':
    if args.eval_mode:
        model = torch.load('./trained_models/street_view_model_100.pth')
        model.eval()
        sum_of_dist = 0
        max_dist = 0
        min_dist = 100000
        for images, lable in DataLoader(val_dataset, batch_size=1):
            images = images.to(device)
            output = model(images).cpu().detach().numpy()
            label = lable.cpu().detach().numpy()
            sum_of_dist += distance.distance(output[0], label[0]).km
            max_dist = max(max_dist, distance.distance(output[0], label[0]).km)
            min_dist = min(min_dist, distance.distance(output[0], label[0]).km)
        print(f"Mean {sum_of_dist / len(val_dataset)}")
        print(f"Max {max_dist}")
        print(f"Min {min_dist}")
        exit()
    for epoch in tqdm(range(args.epochs)):
        model.train()
        train_loss = 0
        for i, (images, labels) in enumerate(DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)):
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        writer.add_scalar('Loss/train', train_loss / len(train_dataset), epoch)
        print(f"Epoch {epoch}, train_loss: {train_loss / len(train_dataset)}")

        if epoch % 10 == 0:
            model.eval()
            val_loss = 0
            with torch.no_grad():
                for images, labels in DataLoader(val_dataset, batch_size=args.batch_size):
                    images, labels = images.to(device), labels.to(device)
                    outputs = model(images)
                    val_loss += loss_fn(outputs, labels).item()
            writer.add_scalar('Loss/val', val_loss / len(val_dataset), epoch)
            print(f"Epoch {epoch}, val_loss: {val_loss / len(val_dataset)}")
        if args.save_model and epoch and epoch % (args.epochs // 3) == 0:
            torch.save(model, f'./trained_models/street_view_model_{epoch}.pth')
            print("Model saved")

    if args.save_model:
        date = datetime.now().strftime("%m-%d")
        torch.save(model, f'./trained_models/street_view_model_{date}.pth')
        print("Model saved")

    writer.flush()
    writer.close()
