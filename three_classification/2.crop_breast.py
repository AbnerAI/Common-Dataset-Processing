# improved crop_breast by abner 2021-5-15
import glob
import cv2
import numpy as np
from PIL import Image
from skimage.measure import label
from skimage import measure
import copy
import os

def crop(img):
    kernel5 = np.ones((5,5), np.uint8)
    thresh = cv2.Canny(img, 0, 60)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel5)
    closing = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel5)
    contours, hierarchy = cv2.findContours(closing.astype(np.uint8),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(contour) for contour in contours]
    i = np.argmax(areas)
    x, y, w, h = cv2.boundingRect(contours[i])

    return img[y:y+h, x:x+w, :]

output_path = '/media/oem/sda21/cxx/breast_all/Video/for_thesis/crop/All_C/'
lists = os.listdir('/media/oem/sda21/cxx/breast_all/Video/for_thesis/original/2022_All_C_Nodules_Original/')
index_ = 0
error_f = open('./error_c.txt','a')
for item in lists:
    index_ += 1
    if not os.path.exists(output_path + '/' + item):
        os.makedirs(output_path + '/' + item)
    ids = glob.glob('/media/oem/sda21/cxx/breast_all/Video/for_thesis/original/2022_All_C_Nodules_Original/'+ item + '/' +'*.jpg')
    print(str(index_) + '/' + str(len(lists)) + ' ' + output_path + '/' + item)
    
    for i in ids:
        full_name = copy.deepcopy(i)
        file_name = os.path.splitext(i)[0][os.path.splitext(i)[0].rfind('/')+1:]
        img = cv2.imdecode(np.fromfile(i, dtype=np.uint8), cv2.IMREAD_COLOR)
        img = crop(img)
        cv2.imencode('.jpg', img)[1].tofile(output_path + '/' + item + '/' + file_name + '.jpg')