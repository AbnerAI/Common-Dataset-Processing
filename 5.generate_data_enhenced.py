import torchvision
import torchvision.transforms as transforms
import numpy as np
from odataset_generated_data_enhenced import BasicDataset
import torch.nn as nn
import torch
from torch import optim
from torch.utils.data import DataLoader
from torch.autograd import Variable
import argparse
from tqdm import tqdm
import logging
import imgaug.augmenters as iaa
import torch.distributed as dist
import torch.multiprocessing as mp
from tensorboardX import SummaryWriter

sometimes = lambda aug: iaa.Sometimes(0.5, aug)
seq = iaa.Sequential([
    sometimes(iaa.OneOf([
        iaa.GaussianBlur(sigma=1),
        iaa.Fliplr(1.0),
        iaa.Flipud(p=1),
        iaa.Sharpen(alpha=1, lightness=(1.5, 2.0)),
        iaa.ContrastNormalization((0.5, 1.5))
    ]))
])

def augmentation(imgs, cate):
    imgs = imgs.numpy()
    imgs = imgs.transpose((0,2,3,1))
#    imgs_aug = seq(images=imgs)
    imgs_aug = imgs_aug.transpose((0,3,1,2))
    imgs_aug = torch.from_numpy(imgs_aug).type(torch.FloatTensor)
    return imgs_aug, cate


def get_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-f",'--fold', metavar='N', type=int, nargs='+', default = 1,
                    help="secelt fold")
    parser.add_argument("-mp",'--mask_path', metavar='N', type=str, nargs='+',default = "./data/mask/", 
                    help="imgpath")
    parser.add_argument("-b",'--batch_size', metavar='N', type=int, nargs='+', default = 200,
                    help="batch_size")
    parser.add_argument("-ep",'--epoch', metavar='N', type=int, nargs='+', default = 200,
                    help="epoch")
    parser.add_argument("-ip",'--img_path', metavar='N', type=str, nargs='+',default ="/data/zhangkun/transtoimg/", 
                    help="imgpath")
    parser.add_argument("-cp",'--csv_path', metavar='N', type=str, nargs='+',default = "/data/zhangkun/solution.xls", 
                    help="csv file path")
    parser.add_argument("-pm",'--pretrain_path', metavar='N', type=str, nargs='+',default ="/data_b/zk/b7m/CP_epoch901_fold1.pth", 
                    help="mode dict path")
    args = parser.parse_args(args=[])
    return args


kwargs={'map_location':lambda storage, loc: storage.cuda(0,1)}
def load_GPUS(model,model_path,kwargs):
    state_dict = torch.load(model_path,**kwargs)
    # create new OrderedDict that does not contain `module.`
    from collections import OrderedDict
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = k[7:] # remove `module.`
        new_state_dict[name] = v
    # load params
    model.load_state_dict(new_state_dict)
    return model

def init_weights(m):
    if type(m) == nn.Conv2d:
        torch.nn.init.xavier_uniform(m.weight)
        # m.bias.data.fill_(0.00001)

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.firstNet = torchvision.models.resnet34(pretrained=True)
        self.firstNet.fc = nn.Linear(512,254)
        # self.secondLine1 = nn.Linear(512,254)
        self.secondLine2 = nn.Linear(254,64)
        self.secondLine3 = nn.Linear(64,2)

    def forward(self, x):
        x = self.firstNet(x)
        # x = self.secondLine1(x)
        x = self.secondLine2(x)
        x = self.secondLine3(x)
        return x


def train():
    writer = SummaryWriter()
    args = get_args()
    mean = [0.5,0.5,0.5]
    std = [0.5,0.5,0.5] 
    datas1 = BasicDataset("/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk/Pure/three/nudules_two/have/two")
    train_loader = DataLoader(datas1, batch_size=args.batch_size, shuffle=True, num_workers=0, pin_memory=True)
    for i,data in enumerate(tqdm(train_loader),0):
        continue
    
if __name__=="__main__":
        train()
    

