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
from model import StreetViewNetViT
from args import args
from custom_loss import CustomLoss
import pandas as pd

data_path = '../data/640x640/'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device {device}")

writer = SummaryWriter()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),

    # Because I am not sure that it will affect StackedImageDataset, so I won't touch it.
    # I think that these 2 lines will affect very much
    # adding flipping, affine pictures into dataset
    # transforms.RandomHorizontalFlip(),
    # transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.8, 1.2)),
    
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])   
])

dataset = StackedImageDataset(data_path, transform=transform)
dataset.label_df = dataset.label_df
train_size = int((1 - args.val_ratio) * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

print('line 39')

model = torch.load('./trained_models/street_view_model_10-25_2.pth')
# model = StreetViewNetViT().to(device)

model.train()
loss_fn = CustomLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

train_losses = []
val_losses = []

print('line 46')

if __name__ == '__main__':
    print('in main! ')
    if args.eval_mode:
        print("successfully get into args.eval_mode!")
        
        # model = torch.load('./trained_models/street_view_model_100.pth')
        # model.eval()
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
            print(f'\rEpoch [{epoch+1}/{args.epochs}], Batch [{i+1}/{len(train_dataset) / args.batch_size}]', end='', flush=True)
        writer.add_scalar('Loss/train', train_loss / len(train_dataset), epoch)
        print(f"Epoch {epoch}, train_loss: {train_loss / len(train_dataset)}")
        train_losses.append(train_loss / len(train_dataset))
        if epoch % 1 == 0:
            model.eval()
            val_loss = 0
            with torch.no_grad():
                for images, labels in DataLoader(val_dataset, batch_size=args.batch_size):
                    images, labels = images.to(device), labels.to(device)
                    outputs = model(images)
                    val_loss += loss_fn(outputs, labels).item()
            writer.add_scalar('Loss/val', val_loss / len(val_dataset), epoch)
            print(f"Epoch {epoch}, val_loss: {val_loss / len(val_dataset)}")
            val_losses.append(val_loss / len(val_dataset))
        if args.save_model:
            date = datetime.now().strftime("%m-%d")
            torch.save(model, f'./trained_models/street_view_model_{date}_{epoch}.pth')
            print("Model saved")
    
        results_df = pd.DataFrame({
            'train_losses': train_losses,
            'Val_losses': val_losses
        })

        results_df.to_csv('losses_record.csv', index=False)
    if args.save_model:
        date = datetime.now().strftime("%m-%d")
        torch.save(model, f'./trained_models/street_view_model_{date}.pth')
        print("Model saved")

    writer.flush()
    writer.close()