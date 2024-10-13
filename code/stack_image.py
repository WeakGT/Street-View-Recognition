import os
from torch.utils.data import Dataset
from PIL import Image
import pandas as pd
import torch
from torchvision import transforms

class StackedImageDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.groups = self._group_images()
        self.label_df = pd.read_csv(os.path.join(root_dir, 'picture_coords.csv'))

    def _group_images(self):
        groups = {}
        for filename in os.listdir(self.root_dir):
            if filename.endswith('.jpg'):
                group_name = filename.rsplit('_', 1)[0]
                if group_name not in groups:
                    groups[group_name] = []
                groups[group_name].append(filename)

        # Ensure that each group has 4 images
        return {k: v for k, v in groups.items() if len(v) == 4}

    def __len__(self):
        return len(self.groups)

    def __getitem__(self, index):
        group_name = list(self.groups.keys())[index]
        image_files = self.groups[group_name]

        images = []
        for img_file in sorted(image_files):
            img_path = os.path.join(self.root_dir, img_file)
            img = Image.open(img_path).convert('RGB')
            if self.transform:
                img = self.transform(img)
            images.append(img)

        # Stack images along the channel dimension
        stacked_images = torch.cat(images, dim=0)
        label = self._get_label(group_name).float()
        return stacked_images, label


    def _get_label(self, group_name):
        index = int(group_name.split('streetview')[-1])
        latitude, longitude = self.label_df.iloc[index]['latitude'], self.label_df.iloc[index]['longitude']
        return torch.tensor([latitude, longitude])
