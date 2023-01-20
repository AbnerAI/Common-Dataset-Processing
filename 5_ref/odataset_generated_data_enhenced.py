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
    def __init__(self,img_path1,img_path2, transform,new_W = 224,new_H=224):
        self.transform = transform
        self.img_path1 = img_path1
        self.img_path2 = img_path2
        self.ids = []
        self.dataname=[]
        self.firstname=[]
        self.cate = []
        self.new_W = new_W
        self.new_H = new_H
        directoryname1 = os.listdir(self.img_path1)
        directoryname2 = os.listdir(self.img_path2)
        directorylen1 = len(directoryname1)
        directorylen2 = len(directoryname2)
        for i,onename in enumerate(directoryname1):
             sedname = os.path.join(self.img_path1,onename)

             seddirname = os.listdir(sedname)
             for j,thrname in enumerate(seddirname):
                  if '.jpg' in os.path.join(sedname,thrname) and not '_new.jpg' in os.path.join(sedname,thrname) and not '_k.jpg' in os.path.join(sedname,thrname) and thrname[0]!='Z':
                    self.ids.append(os.path.join(sedname,thrname))
                    self.cate.append(0)
        
        for i,onename in enumerate(directoryname2):
             sedname = os.path.join(self.img_path2,onename)
             seddirname = os.listdir(sedname)
             for j,thrname in enumerate(seddirname):
                  if '.jpg' in os.path.join(sedname,thrname) and not '_new.jpg' in os.path.join(sedname,thrname) and not '_k.jpg' in os.path.join(sedname,thrname) and thrname[0]!='Z':
                    self.ids.append(os.path.join(sedname,thrname))
                    self.cate.append(1)
    
    def img_pretreatment(self,imgname):
        img = cv2.imdecode(np.fromfile(imgname, dtype=np.uint8), -1)
        # # img = np.asarray(bytearray(resp.read()), dtype="uint8")
        # # img = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # # img = cv2.imread(img,cv2.IMREAD_COLOR)
        # img = cv2.resize(img,(self.new_W,self.new_H))
        # img = cv2.imread(imgname)#Image.open(imgname)#.convert('BGR')
        if self.transform is not None:
            img = self.transform(Image.fromarray(img))
           
        return img



    def __len__(self):
        return len(self.ids)
    
    def __getitem__(self,i):
        img_name = self.ids[i]
        # print(img_name)

#        print(img_name)
        img_cate = self.cate[i]
#        print(img_cate)
        data_img = self.img_pretreatment(img_name)
        data_img = np.asarray(data_img)
        img_cate = np.asarray(img_cate)
        # data_img = data_img/255
        data_img = data_img.astype(float)
        img_cate = img_cate.astype(float)
        # data_img = data_img.transpose((2, 0, 1))
 
 
 
 
        data_img = torch.from_numpy(data_img).type(torch.FloatTensor)
        img_cate = torch.from_numpy(img_cate).type(torch.FloatTensor)
        return {"img":data_img,"cate":img_cate}
#         return {data_img,img_cate}


class BasicDatasetForCrossValid(Dataset):
    def __init__(self,img_path, labels,new_W = 224,new_H=224):
        self.ids = img_path
        self.labels = labels
        self.new_H = new_H
        self.new_W = new_W

    def img_pretreatment(self,img):
        img = cv2.imdecode(np.fromfile(img, dtype=np.uint8), -1)
        img = cv2.resize(img,(self.new_W,self.new_H))
        return img

    def __len__(self):
        return len(self.ids)
    
    def __getitem__(self,i):
        img_name = self.ids[i]
        # print(img_name)
        img_cate = self.labels[i]

        data_img = self.img_pretreatment(img_name)
        data_img = np.asarray(data_img)
        img_cate = np.asarray(img_cate)
        # data_img = data_img/255
        data_img = data_img.astype(float)
        img_cate = img_cate.astype(float)
        # data_img = data_img.transpose((2, 0, 1))
 
 
        data_img = torch.from_numpy(data_img).type(torch.FloatTensor)
        img_cate = torch.from_numpy(img_cate).type(torch.FloatTensor)
        return {"img":data_img,"labels":img_cate,"path":img_name}
