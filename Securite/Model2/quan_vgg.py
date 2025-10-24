import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import init
import math

from .quantization import *

class TinyVGG(nn.Module):
    def __init__(self, num_classes):
        super(TinyVGG, self).__init__()
        self.features = nn.Sequential(
            quan_Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            quan_Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),   
            nn.Dropout2d(p=0.25),           # ? (32, 16, 16)

            quan_Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            quan_Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout2d(p=0.25),              # ? (32, 8, 8)

       )
        self.classifier = nn.Sequential(
            quan_Linear(2048, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

def tinyvgg_quan(num_classes=10):
    """Constructs a TinyVGG model for CIFAR-10 (by default)
  Args:
    num_classes (uint): number of classes
  """
    model = TinyVGG(num_classes)
    return model