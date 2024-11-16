import torch
import torchvision.transforms as transforms
import sys
import os

# 確保將專案根目錄加入 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model import StreetViewNet

'''
import model and make prediction here
'''
country_list = ['United States', 'Australia', 'Thailand', 'Kenya',
                             'South Africa', 'India', 'Canada', 'Finland', 
                             'France', 'New Zealand', 'Singapore', 'Japan', 
                             'Germany']

class Model:
    def __init__(self, model_path):
        checkpoint = torch.load(model_path, map_location='cpu')
        self.model = StreetViewNet(len(country_list))
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()
        self.resize_transform = transforms.Resize((224, 224))

    def predict(self, images, country_options):
        # 假設 images 是一張圖片的 Tensor
        # ressize to 224x224
        # 從 city_options 中挑選出最有可能的城市
        resize_images = []
        for image in images:
            resize_images.append(self.resize_transform(image))
        images = torch.stack(resize_images)

        with torch.no_grad():
            output = self.model(images)
            output = torch.mean(output, dim=0)
            # sort the output in descending order
            print(output)
            output = torch.argsort(output, descending=True)
            print(output)   
            i = 0
            while i < len(output):
                target = output[i]
                if country_list[target] in country_options:
                    break
                else:
                    i += 1
            predicted_city = country_list[target]

            #output = torch.argmax(output).item()
            #predicted_city = country_list[output]
        return predicted_city