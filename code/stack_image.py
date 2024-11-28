import os
from torch.utils.data import Dataset
from PIL import Image
import pandas as pd
import torch
from torchvision import transforms

country_list = ['United States', 'Australia', 'Thailand', 'Kenya',
                             'South Africa', 'India', 'Canada', 'Finland', 
                             'France', 'New Zealand']

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

class SingleImageDataset(Dataset):
    def __init__(self, root_dir, transform=None, is_train=True):
        self.root_dir = root_dir
        self.transform = transform
        if is_train:
            self.label_df = pd.read_csv(os.path.join(root_dir, 'train.csv'))
            self.data_dir = os.path.join(root_dir, 'train')
        else:
            self.label_df = pd.read_csv(os.path.join(root_dir, 'val.csv'))
            self.data_dir = os.path.join(root_dir, 'val')
        self.groups = self._group_images()
        # self.city_list = ['Keelung', 'New Taipei', 'Taipei', 'Taoyuan', 
        #                   'Hsinchu', 'Miaoli', 'Taichung', 'Changhua',
        #                   'Nantou', 'Yunlin', 'Chiayi', 'Tainan',
        #                   'Kaohsiung', 'Pingtung', 'Yilan', 'Hualien',
        #                   'Taitung', 'Penghu', 'Green Island', 'Orchid Island',
        #                   'Kinmen Country', 'Matsu', 'Lienchiang']

    def _group_images(self):
        # groups = {}
        # for filename in os.listdir(self.root_dir):
        #     if filename.endswith('.jpg'):
        #         group_name = filename
        #         if group_name not in groups:
        #             groups[group_name] = []
        #         groups[group_name].append(filename)
        groups = self.label_df['image'].to_list()

        return groups


    def __len__(self):
        return len(self.groups)

    def __getitem__(self, index):
        img_file = self.groups[index]
        # img_file = self.groups[group_name][0]
        img_path = os.path.join(self.data_dir, img_file)
        img = Image.open(img_path).convert('RGB')
        if self.transform:
            img = self.transform(img) 
        label = self._get_label(index)
        return img, label

    def _get_label(self, index):
        # index = int(group_name.split('streetview')[-1])
        # city = self.label_df.iloc[index]['city']
        # city_code = self.city_list.index(city)
        # city_onehot = torch.zeros(len(self.city_list))
        # city_onehot[city_code] = 1


        # city_lat = self.label_df.iloc[index]['latitude']
        # city_long = self.label_df.iloc[index]['longitude']
        country = self.label_df['country'][index]
        country_code = country_list.index(country)
        return torch.tensor(country_code)
