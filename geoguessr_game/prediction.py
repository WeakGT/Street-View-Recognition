import torch
import torchvision.transforms as transforms
import sys

sys.path.append('../code')
from model import StreetViewNet
from stack_image import country_list
'''
import model and make prediction here
'''

class Model:
    def __init__(self, model_path):
        checkpoint = torch.load(model_path, map_location='cpu')
        self.model = StreetViewNet(len(country_list))
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()
        self.resize_transform = transforms.Resize((224, 224))

    def predict(self, images):
        # 假設 images 是四張圖片的 Tensor
        # ressize to 224x224
        resize_images = []
        for image in images:
            resize_images.append(self.resize_transform(image))
        images = torch.stack(resize_images)

        with torch.no_grad():
            output = self.model(images)
            output = torch.mean(output, dim=0)
            output = torch.argmax(output).item()
            predicted_city = country_list[output]
        return predicted_city