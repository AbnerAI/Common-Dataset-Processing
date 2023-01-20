from distutils import file_util
import os
import glob
import random
import shutil

left_right_remain = 5
left_right_remain_h = 5
equal_dis = 10 # len / equal_dis
equal_dis_h = 10
# 基本要求：等间距抽样

base_path = '/media/oem/sda21/cxx/breast_all/Video/for_thesis/crop/'
c_path = os.path.join(base_path, 'All_C')
n_path = os.path.join(base_path, 'All_N')
save_path = '/media/oem/sda21/cxx/breast_all/Video/for_thesis/variable_three_classification/variable_data_equal_dis/'

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
    if c_nodules_count >= equal_dis:
        rem = int(c_nodules_count/equal_dis) #int(c_nodules_count / c_spe_num)
    elif c_nodules_count >= equal_dis - 5:
        rem = int(c_nodules_count/(equal_dis-5)) #int(c_nodules_count / c_spe_num)
    else:
        rem = 1

    if h_nodules_count >= equal_dis_h:
        rem_h = int(h_nodules_count/equal_dis_h)
    elif h_nodules_count >= equal_dis_h - 5:
        rem_h = int(h_nodules_count/(equal_dis_h-5))
    else:
        rem_h = 1

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
        
        c_first_position += left_right_remain

        copy_count = 0
        for idx_ in range(c_nodules_count):
            if c_first_position + idx_*distance > c_nodules_count - left_right_remain:
                break

            file_name = file_lists[c_first_position + idx_*distance]
            if file_name.startswith('C'):
                copy_count += 1
                file_real_path = os.path.join(file_path, file_name)
                # 复制文件
                shutil.copy(file_real_path, dst_path)
         # check spe_num
        if len(os.listdir(dst_path)) == 0:
            shutil.rmtree(dst_path)
            threshold_count -= 1


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
        h_first_position += left_right_remain_h
        copy_count = 0
        for idx_ in range(h_nodules_count):
            if left_right_remain_h + idx_*distance > h_nodules_count - left_right_remain_h:
                break
            
            file_name = file_lists[h_first_position + idx_*distance]
            if file_name.startswith('Z'):
                copy_count += 1
                file_real_path = os.path.join(file_path, file_name)
                # 复制文件
                shutil.copy(file_real_path, dst_path)
        
        # check spe_num
        if len(os.listdir(dst_path)) == 0:
            shutil.rmtree(dst_path)
            threshold_count_h -= 1

print('C-patient num: {}'.format(threshold_count))
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
    if n_nodules_count >= equal_dis:
        rem = int(n_nodules_count/equal_dis) #int(c_nodules_count / c_spe_num)
    elif n_nodules_count >= equal_dis - 5:
        rem = int(n_nodules_count/(equal_dis-5)) #int(c_nodules_count / c_spe_num)
    else:
        rem = 1

    if h_nodules_count >= equal_dis_h:
        rem_h = int(h_nodules_count/equal_dis_h)
    elif h_nodules_count >= equal_dis_h - 5:
        rem_h = int(h_nodules_count/(equal_dis_h-5))
    else:
        rem_h = 1

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
        
        n_first_position += left_right_remain
        copy_count = 0
        for idx_ in range(n_nodules_count):
            if n_first_position + idx_*distance > n_nodules_count - left_right_remain:
                break

            file_name = file_lists[n_first_position + idx_*distance]
            if file_name.startswith('N'):
                copy_count += 1
                file_real_path = os.path.join(file_path, file_name)
                # 复制文件
                shutil.copy(file_real_path, dst_path)
        # check spe_num
        if len(os.listdir(dst_path)) == 0:
            shutil.rmtree(dst_path)
            threshold_count -= 1
    
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
        
        h_first_position += left_right_remain_h
        copy_count = 0
        for idx_ in range(h_nodules_count):
            if left_right_remain_h + idx_*distance > h_nodules_count - left_right_remain_h:
                break

            file_name = file_lists[h_first_position + idx_*distance]
            if file_name.startswith('Z'):
                copy_count += 1
                file_real_path = os.path.join(file_path, file_name)
                # 复制文件
                shutil.copy(file_real_path, dst_path)
        # check spe_num
        if len(os.listdir(dst_path)) == 0:
            shutil.rmtree(dst_path)
            threshold_count_h -= 1

print('N - patient num: {}'.format(threshold_count))
print('H- patient num: {}'.format(threshold_count_h + threshold_count_c_h))