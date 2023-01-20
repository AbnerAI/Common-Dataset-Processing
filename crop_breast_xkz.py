import glob
import cv2
import os
import numpy as np
# 获取all文件夹下的所有图片
ids = glob.glob("/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/save")
#  根据机器不同进行裁剪，裁剪大小自定义，
# 这个坐标是[y0,y1,x0,x1]
# c: bound = [140, 675, 192, 835] # height width
bound = [145, 670, 160, 840] # height width n
base_path_c = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/save/c/'
base_path_n = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/save/n/'

def crop(img,bound):
    return img[bound[0]:bound[1],bound[2]: bound[3]]

# name = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/save/n/3/N21.jpg'
# print(name)
# img = cv2.imdecode(np.fromfile(name, dtype=np.uint8), cv2.IMREAD_COLOR)
# img = crop(img, bound)
# # .tofile()是为了，文件名中文乱码
# # cv2.imencode('.jpg', img)[1].tofile(name)
# cv2.imencode('.jpg', img)[1].tofile('/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/save/C10.jpg')
# exit(0)


# for it in os.listdir(base_path_c):
#     i = base_path_c + it
#     for i_ in os.listdir(i):
#         name = i + '/' + i_
#         print(name)
#         img = cv2.imdecode(np.fromfile(name, dtype=np.uint8), cv2.IMREAD_COLOR)
#         img = crop(img, bound)
#         # .tofile()是为了，文件名中文乱码
#         cv2.imencode('.jpg', img)[1].tofile(name)

for it in os.listdir(base_path_n):
    i = base_path_n + it
    for i_ in os.listdir(i):
        name = i + '/' + i_
        print(name)
        img = cv2.imdecode(np.fromfile(name, dtype=np.uint8), cv2.IMREAD_COLOR)
        img = crop(img, bound)
        # .tofile()是为了，文件名中文乱码
        cv2.imencode('.jpg', img)[1].tofile(name)
        # cv2.imencode('.jpg', img)[1].tofile('/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/save/C10.jpg')