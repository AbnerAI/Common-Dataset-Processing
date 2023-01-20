# 去重
import cv2
import os
import shutil
import numpy as np


'''
function------将img_path中患者的图片与save_path中的图片对比，计算相似度，如果相似度小于threshold，就把图片放入save_path
            
img_path-----之前提取出的所有帧所在位置，这里路径的下一层文件就是患者的文件夹了，用起来比较费劲，路径前面在加几层循环，一次处理一批数据会方便些
save_path-----之前提取出的关键帧所在位置，这里路径的下一层文件就是患者的文件夹了
threshold-----阈值，图片的相似度，默认使用的0.85

'''

nudles_count = 0

def main():
    global nudles_count
    img_dir = os.listdir(img_path)
    record = []
    for i, name in enumerate(img_dir):
        simg_name = img_path+name+"/"
        ssave_name = save_path+name+"/"
        timg_name = os.listdir(simg_name)
        k_flag = 0
        for j, sname in enumerate(timg_name):
            fimg_name = simg_name+sname
            record = []
            record.clear()
            if sname[0]=='C' or sname[0]=='N':
                if not k_flag:
                    for k, tname in enumerate(timg_name):
                        if tname.endswith('_k.jpg'):
                            finasave_img = simg_name+tname
                            name1 = fimg_name
                            name2 = finasave_img
                            img1 = cv2.imdecode(np.fromfile(name1, dtype=np.uint8), -1)
                            img2 = cv2.imdecode(np.fromfile(name2, dtype=np.uint8), 0)
                            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
                            h, w = img2.shape
                            res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
                            record.append(res[0, 0])
                            if not os.path.exists(ssave_name):
                                os.makedirs(ssave_name)
                            k_flag = 1
                            shutil.copy(finasave_img, ssave_name)
                            break
                else:
                    # general operation
                    img1 = cv2.imdecode(np.fromfile(fimg_name, dtype=np.uint8), -1)
                    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
                    res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
                    record.append(res[0, 0])

                record = np.array(record)
                compare = (np.ones((1, record.shape[0])))*threshold # 0.85
                if((compare > record).all()):
                    if not os.path.exists(ssave_name):
                        os.makedirs(ssave_name)
                    print(fimg_name)
                    nudles_count += 1
                    shutil.copy(fimg_name, ssave_name)
            else:
                if not os.path.exists(ssave_name):
                    os.makedirs(ssave_name)
                shutil.copy(fimg_name, ssave_name)


if __name__ == '__main__':
    # /media/oem/sda21/cxx/breast_all/Video/All_Test_To_Pure_By_Nodules_Model_copy
    img_path = "/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/All_C_Crop_zk/"
    save_path = "/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/All_Crop_zk_Del_Repeat/C/"
    threshold = 0.55 # <threshold, will be save.   me: N: 0.6 3423   C:0.53 4200+  zk: N: 0.63 3417    C: 0.55 4126
    main()
    print('count: ', nudles_count)