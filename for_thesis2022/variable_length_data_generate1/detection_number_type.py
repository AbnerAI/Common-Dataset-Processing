from distutils import file_util
import os
import glob
import shutil

# 三分类数据集
# 基本要求：等间距抽样
# /media/oem/sda21/cxx/breast_all/Video/for_thesis/three_classification
patient_num_threshold = 320
output_spe_num_lists = [5, 10, 12, 14, 16, 18, 20]

base_path = '/media/oem/sda21/cxx/breast_all/Video/for_thesis/crop/'
c_path = os.path.join(base_path, 'All_C')
n_path = os.path.join(base_path, 'All_N')

c_lists = os.listdir(c_path)
n_lists = os.listdir(n_path)
print("-static-")

for spe_num in output_spe_num_lists: 
    # C
    threshold_count = 0
    for one_name in c_lists:
        file_path = os.path.join(c_path, one_name)
        file_lists = os.listdir(file_path)
        health_count = 0
        for idx, file_name in enumerate(file_lists):
            if file_name.startswith('Z'):
                health_count += 1

            if health_count >= spe_num:
                threshold_count += 1
                break
    print('c-special num: {} patient num: {}'.format(spe_num, threshold_count))
    
    for one_name in n_lists:
        file_path = os.path.join(n_path, one_name)
        file_lists = os.listdir(file_path)
        health_count = 0
        # 判断帧数是否足够
        for idx, file_name in enumerate(file_lists):
            if file_name.startswith('Z'):
                health_count += 1

            if health_count >= spe_num:
                threshold_count += 1
                break
        
    print('special num: {} patient num: {}'.format(spe_num, threshold_count))
