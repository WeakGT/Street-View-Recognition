import torch
import torchvision.transforms as transforms
import sys
import os
from PIL import Image
from config import country_list

# 確保將專案根目錄加入 sys.path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(project_root)
from model.model import StreetViewNet

class Model:
    def __init__(self, model_path):
        checkpoint = torch.load(os.path.join(project_root, model_path), map_location='cpu')
        self.model = StreetViewNet(len(country_list))
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()
        self.resize_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def predict(self, image_path, country_options):
        # 假設 images 是一張圖片的 Tensor
        # ressize to 224x224
        # 從 city_options 中挑選出最有可能的城市
        # resize_images = []
        # for image in images:
        image = Image.open(image_path).convert('RGB')
        image = self.resize_transform(image)
        image = image.unsqueeze(0)
        # images = torch.stack(resize_images)

        with torch.no_grad():
            output = self.model(image)
            output = torch.mean(output, dim=0)
            # sort the output in descending order
            print(output)
            output = torch.argsort(output, descending=True)
            print(output)   
            i = 0
            while i < len(output):
                target = output[i]
                if country_list[target] in country_options:
                    predicted_city = country_list[target]
                    break
                else:
                    i += 1

            #output = torch.argmax(output).item()
            #predicted_city = country_list[output]
        return predicted_city