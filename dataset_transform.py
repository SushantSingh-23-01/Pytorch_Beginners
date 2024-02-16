import torch
from torch.utils.data import Dataset
import numpy as np
import torchvision

class wineDataset(Dataset):
    def __init__(self,transform = None):
        # Data Loading
        # https://github.com/patrickloeber/pytorchTutorial/blob/master/data/wine/wine.csv
        xy = np.loadtxt('dataset/wine.csv',delimiter= ',',dtype=np.float32,skiprows=1)
        self.n_samples = xy.shape[0]
        self.x = xy[:,1:]
        self.y = xy[:,[0]]

        self.transform  = transform
        
    def __getitem__(self,index):
        sample = self.x[index], self.y[index]
        if self.transform:
            sample = self.transform(sample)
        return sample
    
    def __len__(self):
        return self.n_samples
    
    
class ToTensor:
    def __call__(self,sample):
        inputs, targets = sample
        return torch.from_numpy(inputs), torch.from_numpy(targets)

class MulTransform:
    def __init__(self, factor):
        self.factor = factor
    
    def __call__(self,sample):
        inputs, targets = sample
        inputs *= self.factor
        return inputs, targets
        
dataset = wineDataset(transform=ToTensor())
first_data = dataset[0]
features, labels = first_data
print(f'Without Mul transform: {features}\n')

composed = torchvision.transforms.Compose([ToTensor(),MulTransform(2)])
dataset = wineDataset(transform=composed)
first_data = dataset[0]
features, labels = first_data
print(f'With Mul transform: {features}\n')