import torch
import torch.nn as nn
import torchvision.models as models

try:
    # wide_resnet = torch.load('./trained_models/wide_resnet50.pth')
    vit = models.vit_b_32(pretrained=True)
except FileNotFoundError:
    # wide_resnet = torch.hub.load('pytorch/vision:v0.6.0', 'wide_resnet50_2', pretrained=True)
    # torch.save(wide_resnet, './trained_models/wide_resnet50.pth')
    vit = models.vit_b_32(pretrained=True)
    torch.save(vit, './trained_models/vit.pth')

class StreetViewNet(nn.Module):
    def __init__(self, num_class):
        super(StreetViewNet, self).__init__()
        self.backbone = vit
        self.class_head = nn.Linear(1000, num_class)
        # self.reg_head = nn.Linear(1000, 2)

    def forward(self, x):
        out = self.backbone(x)
        class_output = self.class_head(out)
        # reg_output = self.reg_head(out)
        return class_output

    def get_embedding(self, x):
        return self.backbone(x)
