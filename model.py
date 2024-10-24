import torch
import torch.nn as nn
import torchvision.models as models
import math

# vit = torch.load('./trained_models/street_view_model_10-24_99.pth', weights_only=True, map_location=torch.device('cpu'))

# vit = torch.load('./trained_models/street_view_model_10-24_99.pth')
# Load a pre-trained Vision Transformer (ViT) from torchvision.models
try:
    vit = torch.load('./trained_models/vit.pth')
except FileNotFoundError:
    vit = models.vit_b_32(pretrained=True)
    torch.save(vit, './trained_models/vit.pth')

class StreetViewNetViT(nn.Module):
    def __init__(self):
        super(StreetViewNetViT, self).__init__()
        self.preprocess_conv = nn.Sequential(
            nn.Conv2d(12, 3, (3, 3), padding=1),  # Adjusting input channels from 12 to 3
            nn.ReLU()
        )
        self.vit = vit
        self.fc1 = nn.Linear(1000, 2 + 14 * 8)  # Assuming ViT outputs 1000 features like ResNet
        # 14 : (25.5 - 22) / 0.25 = 14
        # 8: (122 - 120)/0.25 = 8

    def forward(self, x):
        x1 = self.preprocess_conv(x)
        x2 = self.vit(x1)  # Vision Transformer
        x3 = self.fc1(x2)

        pred_class_probs = torch.softmax(x3[:, 2:], dim=1)  # Apply softmax across the class dimension
        predicted_class = torch.argmax(pred_class_probs, dim=1) 
        x_plus = (predicted_class // 8).int() * 0.25 + 22  # 恢复 target_x
        y_plus = (predicted_class % 8).int() * 0.25 + 120  # 恢复 target_y
        x3[:, 0] += x_plus
        x3[:, 1] += y_plus
        return x3
