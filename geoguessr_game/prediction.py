import torch
'''
import model and make prediction here
'''

class Model:
    def __init__(self, model_path):
        self.model = torch.load(model_path)
        self.model.eval()

    def predict(self, images):
        # 假設 images 是四張圖片的 Tensor
        # with torch.no_grad():
            # output = self.model(images)
            # _, predicted_city = torch.max(output, 1)
        # return predicted_city.item()  # 返回預測的城市
        pass