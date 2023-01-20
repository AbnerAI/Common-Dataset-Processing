from distutils import file_util
import os
import glob
import random
import shutil

# 数据集: 1~30帧
max_frame = 25
min_frame = 5

# 基本要求：等间距抽样

base_path = '/media/oem/sda21/cxx/breast_all/Video/for_thesis/crop/'
c_path = os.path.join(base_path, 'All_C')
n_path = os.path.join(base_path, 'All_N')
save_path = '/media/oem/sda21/cxx/breast_all/Video/for_thesis/variable_three_classification/variable_data_5_to_25/'

c_lists = os.listdir(c_path)
n_lists = os.listdir(n_path)

# C
threshold_count = 0
threshold_count_h = 0
for one_name in c_lists:
    file_path = os.path.join(c_path, one_name)
    file_lists = os.listdir(file_path)
    # print(file_lists)
    file_lists.sort(key= lambda x:(x[0], 0 if 'k' in x else int(x[1:-4])))
    
    c_nodules_count = 0
    h_nodules_count = 0
    # 判断C帧数是否足够
    for idx, file_name in enumerate(file_lists):
        if file_name.startswith('C'):
            c_nodules_count += 1
        if file_name.startswith('Z'):
            h_nodules_count += 1
    rem = -1
    rem_h = -1
    if c_nodules_count >= min_frame:
        c_spe_num = random.randint(min_frame,c_nodules_count if c_nodules_count<max_frame else max_frame)
        rem = int(c_nodules_count / c_spe_num)

    if h_nodules_count >= min_frame:
        h_spe_num = random.randint(min_frame,h_nodules_count if h_nodules_count<max_frame else max_frame)
        rem_h = int(h_nodules_count / h_spe_num)

    if rem >= 1:
        threshold_count += 1
        distance = rem
        len_lists = len(file_lists)
        
        # create save_path
        dst_path = os.path.join(save_path, 'C/' + one_name)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        # first c_position detection
        c_first_position = -1
        for idx, file_name in enumerate(file_lists):
            if file_name.startswith('C'):
                c_first_position = idx
                break
        
        copy_count = 0
        for idx_ in range(c_nodules_count):
            file_name = file_lists[c_first_position + idx_*distance]
            if file_name.startswith('C'):
                copy_count += 1
                file_real_path = os.path.join(file_path, file_name)
                # 复制文件
                shutil.copy(file_real_path, dst_path)
                # print(dst_path)
                if copy_count == c_spe_num:
                    break
        # check spe_num
        if len(os.listdir(dst_path)) != c_spe_num:
            shutil.rmtree(dst_path)
    
    if rem_h >= 1:
        threshold_count_h += 1
        distance = rem_h
        len_lists = len(file_lists)
        # create save_path
        dst_path = os.path.join(save_path, 'H/' + one_name)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        # first c_position detection
        h_first_position = -1
        for idx, file_name in enumerate(file_lists):
            if file_name.startswith('Z'):
                h_first_position = idx
                break
        
        copy_count = 0
        for idx_ in range(h_nodules_count):
            file_name = file_lists[h_first_position + idx_*distance]
            if file_name.startswith('Z'):
                copy_count += 1
                file_real_path = os.path.join(file_path, file_name)
                # 复制文件
                shutil.copy(file_real_path, dst_path)
                # print(dst_path)
                if copy_count == h_spe_num:
                    break
        # check spe_num
        if len(os.listdir(dst_path)) != h_spe_num:
            shutil.rmtree(dst_path)

print('Cpatient num: {}'.format(threshold_count))
threshold_count_c_h = threshold_count_h
# N
threshold_count = 0
threshold_count_h = 0
for one_name in n_lists:
    file_path = os.path.join(n_path, one_name)
    file_lists = os.listdir(file_path)
    # 关键帧在第一位，然后是结节帧，最后是健康帧。
    file_lists.sort(key= lambda x:(x[0], 0 if 'k' in x else int(x[1:-4])))
    n_nodules_count = 0
    h_nodules_count = 0
    for idx, file_name in enumerate(file_lists):
        if file_name.startswith('N'):
            n_nodules_count += 1
        if file_name.startswith('Z'):
            h_nodules_count += 1
    
    rem = -1
    rem_h = -1
    if n_nodules_count >= min_frame:
        n_spe_num = random.randint(min_frame,n_nodules_count if n_nodules_count<max_frame else max_frame)
        rem = int(n_nodules_count / n_spe_num)

    if h_nodules_count >= min_frame:
        h_spe_num = random.randint(min_frame,h_nodules_count if h_nodules_count<max_frame else max_frame)
        rem_h = int(h_nodules_count / h_spe_num)

    if rem >= 1:
        threshold_count += 1
        distance = rem
        len_lists = len(file_lists)
        # create save_path
        dst_path = os.path.join(save_path, 'N/' + one_name)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        # first n_position detection
        n_first_position = -1
        for idx, file_name in enumerate(file_lists):
            if file_name.startswith('N'):
                n_first_position = idx
                break
        
        copy_count = 0
        for idx_ in range(n_nodules_count):
            file_name = file_lists[n_first_position + idx_*distance]
            if file_name.startswith('N'):
                copy_count += 1
                file_real_path = os.path.join(file_path, file_name)
                # 复制文件
                shutil.copy(file_real_path, dst_path)
                # print(dst_path)
                if copy_count == n_spe_num:
                    break
        # check spe_num
        if len(os.listdir(dst_path)) != n_spe_num:
            shutil.rmtree(dst_path)
    
    if rem_h >= 1:
        threshold_count_h += 1
        distance = rem_h
        len_lists = len(file_lists)
        # create save_path
        dst_path = os.path.join(save_path, 'H/N_' + one_name)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        # first c_position detection
        h_first_position = -1
        for idx, file_name in enumerate(file_lists):
            if file_name.startswith('Z'):
                h_first_position = idx
                break
        
        copy_count = 0
        for idx_ in range(h_nodules_count):
            file_name = file_lists[h_first_position + idx_*distance]
            if file_name.startswith('Z'):
                copy_count += 1
                file_real_path = os.path.join(file_path, file_name)
                # 复制文件
                shutil.copy(file_real_path, dst_path)
                # print(dst_path)
                if copy_count == h_spe_num:
                    break
        # check spe_num
        if len(os.listdir(dst_path)) != h_spe_num:
            shutil.rmtree(dst_path)

print('N - patient num: {}'.format(threshold_count))
print('H- patient num: {}'.format(threshold_count_h + threshold_count_c_h))