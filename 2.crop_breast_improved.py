# improved crop_breast by abner 2021-5-15
import glob
import cv2
import numpy as np
from PIL import Image
from skimage.measure import label
from skimage import measure

def HandleRows(pp, threshold_black_ratio, stop_threshold_rounds):
    stop_flag = 0
    row_min = 0
    # rows
    for row_ in range(pp.shape[0]//2):
        if (np.sum(pp[row_]==0)/len(pp[row_])) > threshold_black_ratio:
            row_min = row_
        else:
            if stop_flag==0:
                stop_flag += 1
            else:
                stop_flag += 1
                if stop_flag > stop_threshold_rounds:
                    break


    stop_flag = 0
    row_max = 0
    for row_ in range(pp.shape[0]//2):
        row_ = pp.shape[0] - row_- 1
        if (np.sum(pp[row_]==0)/len(pp[row_])) > threshold_black_ratio:
            row_max = pp.shape[0] - row_
        else:
            if stop_flag==0:
                stop_flag += 1
            else:
                stop_flag += 1
                if stop_flag > stop_threshold_rounds:
                    break

    return row_min, row_max

def HandleColumns(pp, threshold_black_ratio, stop_threshold_rounds):
    stop_flag = 0
    column_min = 0
    # for column_ in range(pp.shape[1]):
    for column_ in range(pp.shape[1]//2):
        if (np.sum(pp[:,column_]==0)/len(pp[:,column_])) > threshold_black_ratio:
            column_min = column_
        else:
            if stop_flag==0:
                stop_flag += 1
            else:
                stop_flag += 1
                if stop_flag > stop_threshold_rounds:
                    break
         

    stop_flag = 0
    column_max = 0
    for column_ in range(pp.shape[1]//2):
        column_ = pp.shape[1] - column_ - 1
        if (np.sum(pp[:,column_]==0)/len(pp[:,column_])) > threshold_black_ratio:
            column_max = pp.shape[1] - column_
        else:
            if stop_flag==0:
                stop_flag += 1
            else:
                stop_flag += 1
                if stop_flag > stop_threshold_rounds:
                    break
                
    return column_min, column_max

# 输入二值图像mask>
def GetBoundingBox(bw_image):
    labeled_img, num = measure.label(bw_image, background=0, return_num=True)
    # 这里返回的labeled_img是一幅图像，不再是一副二值图像，有几个连通域，最大值就是几，num是连通域个数，1个连通域的话num=1

    max_label = 0
    max_num = 0
    # 图像全黑，没有连通域num=0,或者是由一个连通域num=1，直接返回原图像
    if num == 0 or num == 1:
        return bw_image
    else:
        for i in range(1, num+1):  #注意这里的范围，为了与连通域的数值相对应
            # 计算面积，保留最大面积对应的索引标签，然后返回二值化最大连通域
            if np.sum(labeled_img == i) > max_num:
                max_num = np.sum(labeled_img == i)
                max_label = i
        lcc = (labeled_img == max_label)
        return lcc

import copy
import os 

output_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/All_N_Crop'
lists = os.listdir('/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/All_N')
index_ = 0
error_f = open('./error_n.txt','a')
for item in lists:
    index_ += 1
    if not os.path.exists(output_path + '/' + item):
        os.mkdir(output_path + '/' + item)
    ids = glob.glob('/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/All_N/'+ item + '/' +'*.jpg')
    print(str(index_) + '/' + str(len(lists)) + ' ' + output_path + '/' + item)
    
    vote_threshold = 10
    row_threshold = list() #[0 for i in range(vote_value_num_max)] 
    column_threshold = list() #[0 for i in range(vote_value_num_max)]

    row_min_threshold = -1
    row_max_threshold = -1
    column_min_threshold = -1
    column_max_threshold = -1

    ind_count = 0

    for i in ids:
        if not ind_count:
            ind_count = 1
            # print(i)
            full_name = copy.deepcopy(i)
            file_name = os.path.splitext(i)[0][os.path.splitext(i)[0].rfind('/')+1:]
            img = cv2.imdecode(np.fromfile(i, dtype=np.uint8), cv2.IMREAD_COLOR)
            # img = cv2.imread("/home/qianxianserver/data/cxx/breast_all/混合乳腺数据/乳腺/2021恶性/175/C14.jpg")
            # img = cv2.medianBlur(img, 3)
            gray1 = img#cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # cv2.namedWindow('original', cv2.WINDOW_AUTOSIZE)
            gray = copy.deepcopy(gray1)
            # cv2.imshow('original', gray)

            gray[gray<=2] = 0
            gray[gray>2] = 255
            ff = GetBoundingBox(gray).astype(float)
            x_min, x_max, y_min, y_max = min(np.where(ff == 1)[0]), max(np.where(ff == 1)[0]), min(np.where(ff == 1)[1]), max(np.where(ff == 1)[1])  
            pp = gray[x_min:x_max, y_min:y_max]
            
            row_min = 0
            row_max = 0
            column_min = 0
            column_max = 0
            threshold_black_ratio = 0.7
            stop_threshold_rounds = 5
            
            row_min, row_max =  HandleRows(pp, threshold_black_ratio, stop_threshold_rounds)
            column_min, column_max =  HandleColumns(pp, threshold_black_ratio, stop_threshold_rounds)
            x_min = x_min + row_min + 5
            x_max = x_max - row_max - 5
            y_min = y_min + column_min + 5
            y_max = y_max - column_max - 5
            crop_after_original = gray1[x_min:x_max, y_min:y_max, :]

            row_min_threshold = x_min
            row_max_threshold = x_max

            column_min_threshold = y_min
            column_max_threshold = y_max

            row_threshold.append(crop_after_original.shape[0])
            column_threshold.append(crop_after_original.shape[1])

            # cv2.imshow('ff', ff)
            # cv2.imshow('pp', pp)
            # cv2.imshow('crop_after_original', crop_after_original)
            cv2.imencode('.jpg', crop_after_original)[1].tofile(output_path + '/' + item + '/' + file_name + '.jpg')

            # cv2.waitKey()
            # cv2.destroyAllWindows()
            # exit(0)
        else:
            file_name = os.path.splitext(i)[0][os.path.splitext(i)[0].rfind('/')+1:]
            img = cv2.imdecode(np.fromfile(i, dtype=np.uint8), cv2.IMREAD_COLOR)
            gray1 = img#cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            crop_after_original = gray1[row_min_threshold:row_max_threshold, column_min_threshold:column_max_threshold,:]
            cv2.imencode('.jpg', crop_after_original)[1].tofile(output_path + '/' + item + '/' + file_name + '.jpg')