#-*-coding:GBK -*-
import xlrd
from torch.utils.data import Dataset
import csv
import cv2
import os
import torch
from PIL import Image
import numpy as np
import torchvision.transforms as transforms
class BasicDataset(Dataset):
    def __init__(self,img_path):
        self.img_path1 = img_path
        self.ids = []
        for root,dirs,files in os.walk(self.img_path1):
            for name in files:
                if '.jpg' in os.path.join(root,name) and name[0]!='Z':
                    self.ids.append(os.path.join(root,name))
    
    def img_pretreatment(self,imgname):
        transform1 = transforms.Compose([transforms.RandomVerticalFlip(p=1)])
        transform2 = transforms.Compose([transforms.RandomVerticalFlip(p=1) ,transforms.RandomHorizontalFlip(p=1)])
        transform3 = transforms.Compose([transforms.RandomHorizontalFlip(p=1)])

        img = cv2.imdecode(np.fromfile(imgname, dtype=np.uint8), -1)


        img_ = transform1(Image.fromarray(img))
        data_img = np.asarray(img_)
        cv2.imencode('.jpg', data_img)[1].tofile(imgname[:-4] + '_en1.jpg')

        img_ = transform2(Image.fromarray(img))
        data_img = np.asarray(img_)
        # cv2.imencode('.jpg', data_img)[1].tofile(imgname[:-4] + '_en2.jpg')

        img_ = transform3(Image.fromarray(img))
        data_img = np.asarray(img_)
        # cv2.imencode('.jpg', data_img)[1].tofile(imgname[:-4] + '_en3.jpg')
        return True

    def __len__(self):
        return len(self.ids)
    
    def __getitem__(self,i):
        img_name = self.ids[i]
        data_img = self.img_pretreatment(img_name)
        return True