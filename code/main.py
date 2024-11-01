import os
import numpy as np
from geopy import distance
import matplotlib.pyplot as plt
from sklearn.utils.class_weight import compute_class_weight
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch.nn import CrossEntropyLoss, MSELoss
from torcheval.metrics.classification import MulticlassF1Score
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from datetime import datetime
from stack_image import StackedImageDataset, SingleImageDataset
from model import StreetViewNet
from args import args

data_path = '../processed/'


# available_gpus = [i for i in range(torch.cuda.device_count())]
# least_used_gpu = min(available_gpus, key=lambda i: torch.cuda.memory_reserved(i))
# torch.cuda.set_device(least_used_gpu)
# device = least_used_gpu
device = torch.device('cuda:1' if torch.cuda.is_available() else 'cpu')
print(f"Using device {device}")
start_time = datetime.now().strftime("%m-%d-%H-%M")

writer = SummaryWriter()

transform = transforms.Compose([
    # transforms.RandomCrop(80),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1),
    # transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.8, 1.2)),
    
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

standard_transform = transforms.Compose([
    # transforms.RandomCrop(80),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

generator = torch.Generator().manual_seed(args.random_seed)
train_dataset = SingleImageDataset(data_path, transform=transform, is_train=True)
val_dataset = SingleImageDataset(data_path, transform=standard_transform, is_train=False)
num_class = len(train_dataset.country_list)

model = StreetViewNet(num_class=num_class).to(device)
# Calculated the data weights first
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(train_dataset.label_df['country'].values),
    y=train_dataset.label_df['country'].values
)
class_weights = torch.FloatTensor(class_weights).to(device)
class_lossfn = CrossEntropyLoss(label_smoothing=args.label_smoothing, weight=class_weights)
reg_lossfn = MSELoss()
f1_metric = MulticlassF1Score(num_classes=num_class, average='macro')

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
    # Start training
    for epoch in tqdm(range(start_epoch, args.epochs)):
        model = model.train()
        train_loss = 0
        correct_count = 0
        f1_metric.reset()
        best_f1 = 0
        best_checkpoint = {}
        for i, (img, label) in enumerate(DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=args.load_data_workers, pin_memory=True, generator=generator)):
            img = img.to(device)
            label = label.to(device).long()
            # class_label, reg_label = label
            # class_label = class_label.to(device).long()
            # reg_label = reg_label.to(device).float()
            class_pred = model(img)

            optimizer.zero_grad()
            class_loss = class_lossfn(class_pred, label)
            # reg_loss = reg_lossfn(reg_pred, reg_label).to(torch.float32)
            # total_loss = (class_loss + args.alpha * reg_loss)
            # total_loss.backward()
            class_loss.backward()
            
            optimizer.step()
            train_loss += class_loss.item()
            f1_metric.update(class_pred, label)
            correct_count += (class_pred.argmax(dim=1) == label).sum().item()

        f1_score = f1_metric.compute()
        writer.add_scalar('Loss/train', train_loss / len(train_dataset), epoch)
        writer.add_scalar('f1_score/train', f1_score, epoch)
        print(f"Epoch {epoch}, train_loss: {train_loss / len(train_dataset)}")
        print(f"Epoch {epoch}, train_f1: {f1_score}")
        print(f"Epoch {epoch}, train_accuracy: {correct_count / len(train_dataset)}")


        # Run the validation
        model.eval()
        val_loss = 0
        correct_count = 0
        f1_metric.reset()
        with torch.no_grad():
            for img, label in DataLoader(val_dataset, batch_size=args.batch_size):
                img = img.to(device)
                label = label.to(device).long()
                # class_label, reg_label = label
                # class_label = class_label.to(device)
                # reg_label = reg_label.to(device)
                class_pred = model(img) 
                class_loss = class_lossfn(class_pred, label)
                # reg_loss = reg_lossfn(reg_pred, reg_label)
                # total_loss = (class_loss + args.alpha * reg_loss)
                val_loss += class_loss.item()
                f1_metric.update(class_pred, label)
                correct_count += (class_pred.argmax(dim=1) == label).sum().item()
        f1_score = f1_metric.compute()
        writer.add_scalar('Loss/val', val_loss / len(val_dataset), epoch)
        writer.add_scalar('f1_score/val', f1_score, epoch)
        print(f"Epoch {epoch}, val_loss: {val_loss / len(val_dataset)}")
        print(f"Epoch {epoch}, val_f1: {f1_score}")
        print(f"Epoch {epoch}, val_accuracy: {correct_count / len(val_dataset)}")
        # validation end

        # save model every checkpoint_step epochs
        if (epoch+1) % args.checkpoint_step == 0 or (epoch+1) == args.epochs:
            if not os.path.exists(f'./trained_models/{start_time}'):
                os.makedirs(f'./trained_models/{start_time}')
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
            }, f'./trained_models/{start_time}/model-{epoch}.pth')
            print("Model saved")
        elif f1_score > best_f1:
            best_f1 = f1_score
            best_checkpoint.clear()
            best_checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
            } 

    if best_checkpoint != {}:
        best_epoch = best_checkpoint['epoch']
        torch.save(best_checkpoint, f'./trained_models/{start_time}/best_model_{best_epoch}.pth')
        print("Best model saved")

    writer.flush()
    writer.close()
