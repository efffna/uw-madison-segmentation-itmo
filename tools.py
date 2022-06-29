import torch
from torch import nn
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import torch
import cv2
from torchvision import transforms


PATH_MODEL = 'models/torchscript.pt'
PATH_MASK = 'temp/mask.png'
PATH_OUT = 'temp/out.png'

class Segmentation:
    def __init__(self):
        self.img_size = 224
        self.model = self.load_model()
        self.preproc_image = None 
        self.original_image = None

    def load_model(self):
        model = torch.jit.load(PATH_MODEL, map_location='cpu')
        return model

    def preprocessing(self, bytes):
        image = np.asarray(bytearray(bytes), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
        image = cv2.resize(image, (self.img_size,self.img_size)) 
        self.original_image = image
        image = np.tile(image[...,None], [1, 1, 3]).astype('float32') 
        mx = np.max(image)
        if mx:
            image/=mx 
        image = np.transpose(image, (2, 0, 1))
        image = np.expand_dims(image,axis=0)
        image = torch.tensor(image,dtype=torch.float32)
        self.preproc_image = image

    def get_predict(self):
        pred = self.model(self.preproc_image )
        mask = (nn.Sigmoid()(pred)>0.5).double()
        mask = torch.mean(torch.stack([mask], dim=0), dim=0)
        mask = (mask[0].permute((1,2,0))>0.5).to(torch.uint8).cpu().detach().numpy() * 255 
        cv2.imwrite(PATH_MASK, mask)
        self.show_img(mask)

    def show_img(self,mask=None):
        fig = plt.figure()
        plt.imshow(self.original_image, cmap='bone')
        if mask is not None:
            plt.imshow(mask, alpha=0.5)
            handles = [Rectangle((0,0),1,1, color=_c) for _c in [(0.667,0.0,0.0), (0.0,0.667,0.0), (0.0,0.0,0.667)]]
            labels = ["Large Bowel", "Small Bowel", "Stomach"]
            plt.legend(handles,labels)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(PATH_OUT,bbox_inches='tight')