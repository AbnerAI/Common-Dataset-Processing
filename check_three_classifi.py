import os
import shutil

base_path_c = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/All_C_New/'
base_path_n = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/All_N_New/'

all_c = os.listdir(base_path_c)
all_n = os.listdir(base_path_n)

cn_flag = 0
h_flag = 0

for i in all_c:
    file_name = base_path_c + i
    save_all_img = os.listdir(file_name)
    nudules_flag = 0
    health_flag = 0
    key_flag = 0

    for img_ in save_all_img:
        if img_[0] == 'C' or img_[0] == 'N':
            nudules_flag = 1
        if img_[0] == 'Z':
            health_flag = 1
        if img_.endswith('_k.jpg'):
            key_flag = 1
        if key_flag + health_flag + nudules_flag == 3:
            break
           
    if key_flag + health_flag + nudules_flag != 3:
        shutil.rmtree(file_name)
        print(file_name)