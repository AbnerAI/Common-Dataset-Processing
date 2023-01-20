import torchvision
import torchvision.transforms as transforms
import numpy as np
from NET import xception
from odataset import BasicDataset
import torch.nn as nn
import torch
from torch import optim
from torch.utils.data import DataLoader
from torch.autograd import Variable
import argparse
from tqdm import tqdm
import logging
import imgaug.augmenters as iaa
from model.model import EfficientNet
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
    
    # /home/qianxianserver/data/cxx/ultrasound_data/勾画图片及json/DataIncludeKeyFrame

    # transform = transforms.Compose([transforms.RandomVerticalFlip(p=0.5) ,transforms.RandomHorizontalFlip(p=0.5), transforms.RandomRotation(30), transforms.Resize([234,234]), transforms.CenterCrop((224,224)), transforms.ToTensor(), transforms.Normalize(mean, std)])
    transform = transforms.Compose([transforms.RandomVerticalFlip(p=0.5) ,transforms.RandomHorizontalFlip(p=0.5), transforms.RandomRotation(30), transforms.Resize([224,224]), transforms.ToTensor(), transforms.Normalize(mean, std)])
    # transform = transforms.Compose([transforms.Resize([224,224]), transforms.ToTensor(), transforms.Normalize(mean, std)])
    # datas1 = BasicDataset("/home/qianxianserver/data/cxx/1.10/湘雅all/C","/home/qianxianserver/data/cxx/1.10/湘雅all/N")
    # datas1 = BasicDataset("/home/qianxianserver/data/cxx/ultrasound20210312FinalTwoClassification/ultrasound/6-get_hy_key_frame/all_tj_data_have_key_frame/New/Train/C","/home/qianxianserver/data/cxx/ultrasound20210312FinalTwoClassification/ultrasound/6-get_hy_key_frame/all_tj_data_have_key_frame/New/Train/N", transform=transform)
    # datas1 = BasicDataset("/home/qianxianserver/data/cxx/ultrasound20210312FinalTwoClassification/ultrasound/6-get_hy_key_frame/tj_data_hy_2020_have_key_frame/New/Train/C","/home/qianxianserver/data/cxx/ultrasound20210312FinalTwoClassification/ultrasound/6-get_hy_key_frame/tj_data_hy_2020_have_key_frame/New/Train/N", transform=transform)
    # datas1 = BasicDataset("/home/qianxianserver/data/cxx/ultrasound20210312FinalTwoClassification/ultrasound/6-get_hy_key_frame/all_tj_data_have_key_frame/New/Train/C","/home/qianxianserver/data/cxx/ultrasound20210312FinalTwoClassification/ultrasound/6-get_hy_key_frame/all_tj_data_have_key_frame/New/Train/N", transform=transform)
    # datas1 = BasicDataset("/data_b/zk/处理后/二期/C","/data_b/zk/处理后/二期/N")
    
    # hy data
    # datas1 = BasicDataset("/home/qianxianserver/data/cxx/breast_all/混合乳腺数据/乳腺/2021_breast_three_classification/Pure/New/Train/C","/home/qianxianserver/data/cxx/breast_all/混合乳腺数据/乳腺/2021_breast_three_classification/Pure/New/Train/N", transform=transform)
    # datas1 = BasicDataset("/home/qianxianserver/data/cxx/ultrasound_data/勾画图片及json/DataForDivideTest/New/Train/C","/home/qianxianserver/data/cxx/ultrasound_data/勾画图片及json/DataForDivideTest/New/Train/N", transform=transform)
    datas1 = BasicDataset("/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk/Pure/New/Train/C","/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk/Pure/New/Train/N",  transform=transform)
    # datas1 = BasicDataset("/home/qianxianserver/data/cxx/ultrasound_data/勾画图片及json/DataIncludeKeyFrame/C","/home/qianxianserver/data/cxx/ultrasound_data/勾画图片及json/DataIncludeKeyFrame/N",  transform=transform)

    # datas1 = BasicDataset("/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/C_N_0524/New/Train/C","/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/C_N_0524/New/Train/N",  transform=transform)

    print("训练集数据量%d"%(len(datas1)))
    train_loader = DataLoader(datas1, batch_size=args.batch_size, shuffle=True, num_workers=16, pin_memory=True)
    
    transform = transforms.Compose([transforms.Resize([224,224]), transforms.ToTensor(), transforms.Normalize(mean, std)])
    # datas2 = BasicDataset("/home/qianxianserver/data/cxx/ultrasound20210312FinalTwoClassification/ultrasound/6-get_hy_key_frame/tj_data_hy_2020_have_key_frame/New/Test/C","/home/qianxianserver/data/cxx/ultrasound20210312FinalTwoClassification/ultrasound/6-get_hy_key_frame/tj_data_hy_2020_have_key_frame/New/Test/N", transform=transform)
    # datas2 = BasicDataset("/home/qianxianserver/data/cxx/ultrasound20210312FinalTwoClassification/ultrasound/6-get_hy_key_frame/all_tj_data_have_key_frame/New/Test/C","/home/qianxianserver/data/cxx/ultrasound20210312FinalTwoClassification/ultrasound/6-get_hy_key_frame/all_tj_data_have_key_frame/New/Test/N", transform=transform)
    # datas2 = BasicDataset("/home/qianxianserver/data/cxx/ultrasound20210312FinalTwoClassification/ultrasound/6-get_hy_key_frame/all_tj_data_have_key_frame/New/Test/C","/home/qianxianserver/data/cxx/ultrasound20210312FinalTwoClassification/ultrasound/6-get_hy_key_frame/all_tj_data_have_key_frame/New/Test/N", transform=transform)
    
    # hy data
    # datas2 = BasicDataset("/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/C_N_0524/New/Test/C","/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/C_N_0524/New/Test/N",  transform=transform)
    datas2 = BasicDataset("/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk/Pure/New/Test/C","/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk/Pure/New/Test/N",  transform=transform)

    # datas2 = BasicDataset("/home/qianxianserver/data/cxx/ultrasound_data/勾画图片及json/DataForDivideTest/New/Test/C","/home/qianxianserver/data/cxx/ultrasound_data/勾画图片及json/DataForDivideTest/New/Test/N", transform=transform)
    # datas2 = BasicDataset("/home/qianxianserver/data/cxx/breast_all/混合乳腺数据/乳腺/2021_breast_three_classification/Pure/New/Test/C","/home/qianxianserver/data/cxx/breast_all/混合乳腺数据/乳腺/2021_breast_three_classification/Pure/New/Test/N", transform=transform)
    test_loader = DataLoader(datas2, batch_size=args.batch_size, shuffle=True, num_workers=16, pin_memory=True)
    
    net = Net()
    print(net)
    net=net.cuda()

    criterion = nn.CrossEntropyLoss()
#     criterion = nn.MSELoss()
    Loss_list = []
    TraAccuracy_list = []
    ValAccuracy_list = []

    C=0
    N=0
    eval_acc = 0
    optimizer  = optim.Adam(net.parameters(), lr=0.00001)
    batchnumber = 0
    import random
    for epoch in range(args.epoch):
        test_acc = 0
        running_loss = 0
        count = 0
        models_path="./models_path/"
        for i,data in enumerate(tqdm(train_loader),0):
            inputs =data["img"]
            labels =data["cate"]
            for df,mj in enumerate(labels.cpu().numpy()):
               if(mj==0):
                  C=C+1
               elif(mj==1):
                  N=N+1
            # inputs, labels = augmentation(inputs, labels)
            inputs, labels = Variable(inputs), Variable(labels)
            inputs= inputs.cuda()
            labels= labels.cuda()
            optimizer.zero_grad()
            
            # print(inputs.shape)
            # print(labels.shape)
            # exit(0)
            
            outputs = net(inputs)
            batchnumber = batchnumber+1
            labels = labels.long().cuda()
            loss= criterion(outputs , labels).cuda()
            outputs1 = outputs.cpu()
            outputs1 = torch.argmax(outputs1, -1)
            outputs1 = outputs1.numpy()
            outputs1[outputs1>0.5]=1
            outputs1[outputs1<=0.5]=0
            outputs1 = outputs1.astype(np.int)
            labels1 = labels.cpu().numpy()
            labels1 = labels1.astype(np.int)

            test_acc = test_acc + np.sum(outputs1==labels1)
            count+=1
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            # print('loss item: ', loss.item())
        floss =  (running_loss/count)    
        Loss_list.append(floss)
        print("floss:%f"%floss)
        print("train_acc:%f"%(test_acc/(len(datas1))))
        train_acc = test_acc/(len(datas1))
        writer.add_scalar("train_acc", train_acc , epoch )
        floss = 0
        optimizer.step()
        if epoch % 5 == 0:
            # print("保存model")
            # torch.save(net.state_dict(), models_path+ f'CP_epoch{epoch + 1000}_fold{args.fold}.pth')
            # print("保存完成，开始val")
            net.eval()
            loss_regression_ls = []
            loss_classification_ls = []
            val_acc = 0
            print("val集大小:%d"%(len(datas2)))
            for i,data in enumerate(tqdm(test_loader),0):
                with torch.no_grad():
                    inputs =data["img"]
                    labels =data["cate"]
                    inputs, labels = Variable(inputs), Variable(labels)
                    inputs= inputs.cuda()
                    labels= labels.cuda()
                    outputs = net(inputs)
                    
                    outputs = outputs.cpu()
                    outputs = torch.argmax(outputs, -1)
                    outputs = outputs.numpy()
                    outputs[outputs>0.5]=1
                    outputs[outputs<=0.5]=0
                    outputs = outputs.astype(np.int)
                    labels = labels.cpu().numpy()
                    labels = labels.astype(np.int)

                    val_acc = val_acc + np.sum(outputs==labels)
            print("val_acc:%f"%(val_acc/(len(datas2))))
            val = val_acc/(len(datas2))
            if val > eval_acc:
                eval_acc = val
                torch.save(net.state_dict(), models_path+ f'CP_epoch{epoch}_fold{args.fold}_eval_acc_{val}.pth')
            writer.add_scalar("val_acc", val , epoch )
            print("验证完成\n")
            net.train()   

    print("Finished Training")
    writer.close()



if __name__=="__main__":
        train()
    

