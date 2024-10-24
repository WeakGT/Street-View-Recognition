import os
import numpy as np
from geopy import distance
import matplotlib.pyplot as plt
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch.nn import CrossEntropyLoss, MSELoss
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from datetime import datetime
from stack_image import StackedImageDataset, SingleImageDataset
from model import StreetViewNet
from args import args

data_path = '../data/256x256/'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device {device}")
start_time = datetime.now().strftime("%m-%d-%H-%M")

writer = SummaryWriter()

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),

    # Because I am not sure that it will affect StackedImageDataset, so I won't touch it.
    # I think that these 2 lines will affect very much
    # adding flipping, affine pictures into dataset
    transforms.RandomHorizontalFlip(p=0.5),
    # transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.8, 1.2)),
    
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

generator = torch.Generator().manual_seed(args.random_seed)
dataset = SingleImageDataset(data_path, transform=transform)
train_size = int((1 - args.val_ratio) * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size], generator=generator)

model = StreetViewNet().to(device)
class_lossfn = CrossEntropyLoss()
reg_lossfn = MSELoss()

optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
start_epoch = 0
if args.start_from_last:
    try:
        checkpoint = torch.load('./trained_models/cl.pth')
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        start_epoch = checkpoint['epoch'] + 1
        print(f'Resuming training from epoch {start_epoch}')
    except FileNotFoundError:
        pass

if __name__ == '__main__':
    for epoch in tqdm(range(start_epoch, args.epochs)):
        model = model.train()
        train_loss = 0
        for i, (img, label) in enumerate(DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=args.load_data_workers, pin_memory=True)):
            img = img.to(device)
            class_label, reg_label = label
            class_label = class_label.to(device).long()
            reg_label = reg_label.to(device).float()
            class_pred, reg_pred = model(img)

            optimizer.zero_grad()
            class_loss = class_lossfn(class_pred, class_label)
            reg_loss = reg_lossfn(reg_pred, reg_label).to(torch.float32)
            total_loss = (class_loss + args.alpha * reg_loss)
            total_loss.backward()
            
            optimizer.step()
            train_loss += total_loss.item()

        writer.add_scalar('Loss/train', train_loss / len(train_dataset), epoch)
        print(f"Epoch {epoch}, train_loss: {train_loss / len(train_dataset)}")


        # Run the validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for img, label in DataLoader(val_dataset, batch_size=args.batch_size):
                img = img.to(device)
                class_label, reg_label = label
                class_label = class_label.to(device)
                reg_label = reg_label.to(device)
                class_pred, reg_pred = model(img) 
                class_loss = class_lossfn(class_pred, class_label)
                reg_loss = reg_lossfn(reg_pred, reg_label)
                total_loss = (class_loss + args.alpha * reg_loss)
                val_loss += total_loss.item()
        writer.add_scalar('Loss/val', val_loss / len(val_dataset), epoch)
        print(f"Epoch {epoch}, val_loss: {val_loss / len(val_dataset)}")
        # validation end

        # save model every checkpoint_step epochs
        if epoch % args.checkpoint_step == 0:
            if not os.path.exists(f'./trained_models/{start_time}'):
                os.makedirs(f'./trained_models/{start_time}')
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
            }, f'./trained_models/{start_time}/model-{epoch}.pth')
            print("Model saved")

    writer.flush()
    writer.close()
