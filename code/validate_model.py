import torch
from model import StreetViewNet
from stack_image import SingleImageDataset
from torchvision import transforms
from torch.utils.data import DataLoader
from sklearn.manifold import TSNE
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
checkpoint = torch.load('./trained_models/11-20-19-32/model-49.pth')
model = StreetViewNet().to(device)
model.load_state_dict(checkpoint['model_state_dict'])
model = model.eval()

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
val = SingleImageDataset('../data/256x256/', transform=transform)
train_dataset, val_dataset = torch.utils.data.random_split(val, [0.8, 0.2])

if __name__ == '__main__':
    correct_pred_class = 0
    pred_embeddings = []
    class_labels = []
    classes_stats = {i: 0 for i in range(23)}
    for i, (img, label) in enumerate(DataLoader(val_dataset, batch_size=8, shuffle=True, num_workers=6, pin_memory=True)):
        img = img.to(device)
        class_label, reg_label = label
        class_label = class_label.to(device).long()
        reg_label = reg_label.to(device).float()
        class_pred, reg_pred = model(img)
        correct_pred_class += (class_pred.argmax(1) == class_label).sum().item()

        embedding = model.get_embedding(img).detach().cpu().numpy()
        pred_embeddings.append(embedding)
        class_labels.append(class_label.cpu().numpy())
        for i in range(8):
            classes_stats[class_label[i].item()] += 1
    print(f"Accuracy: {correct_pred_class / len(val_dataset)}")

    pred_embeddings = np.concatenate(pred_embeddings, axis=0)
    class_labels = np.concatenate(class_labels, axis=0)
    print(pred_embeddings.shape)
    tsne_embedding = TSNE(n_components=2, random_state=0).fit_transform(pred_embeddings)
    ax = sns.scatterplot(x=tsne_embedding[:, 0], y=tsne_embedding[:, 1], hue=class_labels, alpha=0.5, palette="tab10")

    plt.figure(figsize=(10, 10))
    plt.bar(classes_stats.keys(), classes_stats.values())
    plt.xlabel('Class')
    plt.ylabel('Count')
    plt.title('Class distribution')

    plt.show()
    


