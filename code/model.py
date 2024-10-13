import torch
import torch.nn as nn

try:
    wide_resnet = torch.load('./trained_models/wide_resnet50.pth')
except FileNotFoundError:
    wide_resnet = torch.hub.load('pytorch/vision:v0.6.0', 'wide_resnet50_2', pretrained=True)
    torch.save(wide_resnet, './trained_models/wide_resnet50.pth')

class StreetViewNet(nn.Module):
    def __init__(self):
        super(StreetViewNet, self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(12, 3, (3, 3), padding=1),
            nn.ReLU(),
            wide_resnet,
            nn.Linear(1000, 2)
        )

    def forward(self, x):
        return self.model(x)