from distutils import file_util
import os
import glob
import shutil

# 基本要求：包含关键帧
patient_num_threshold = 320
output_spe_num_lists = [5, 10, 12, 14, 16, 18, 20]

base_path = '/media/oem/sda21/cxx/breast_all/Video/for_thesis/crop/'
c_path = os.path.join(base_path, 'All_C')
n_path = os.path.join(base_path, 'All_N')
base_output_path = '/media/oem/sda21/cxx/breast_all/Video/for_thesis/spe_num'

c_lists = os.listdir(c_path)
n_lists = os.listdir(n_path)
print("-static-")

for spe_num in output_spe_num_lists: 
    save_path = os.path.join(base_output_path, str(spe_num))

    # C
    threshold_count = 0
    for one_name in c_lists:
        file_path = os.path.join(c_path, one_name)
        file_lists = os.listdir(file_path)
        k_position = -1
        c_nodules_count = 0
        # 判断帧数是否足够
        for idx, file_name in enumerate(file_lists):
            if file_name.endswith('k.jpg'):
                k_position = idx
            if file_name.startswith('C'):
                c_nodules_count += 1

        copy_count = 0

        if c_nodules_count >= spe_num:
            if threshold_count == patient_num_threshold:
                break
            threshold_count += 1
            
            # create save_path
            dst_path = os.path.join(save_path, 'C/' + one_name)
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            # z_position detection
            z_position = -1
            for idx, file_name in enumerate(file_lists):
                if file_name.startswith('Z'):
                    z_position = idx

            len_lists = len(file_lists)
            file_name = file_lists[k_position]
            file_real_path = os.path.join(file_path, file_name)
            # 复制关键帧
            shutil.copy(file_real_path, dst_path)
            copy_count += 1
            if copy_count == spe_num:
                print('task finished.')
                exit(0)
            # print(dst_path)
            
            # left & right
            for idx_ in range(1, len_lists):
                if k_position - idx_ >= 0:
                    # left
                    file_name = file_lists[k_position-idx_]
                    if file_name.startswith('C'):
                        copy_count += 1
                        file_real_path = os.path.join(file_path, file_name)
                        # 复制文件
                        shutil.copy(file_real_path, dst_path)
                        # print(dst_path)
                        if copy_count == spe_num:
                            break

                # right
                if k_position + idx_ < z_position:
                    file_name = file_lists[k_position+idx_]
                    if file_name.startswith('C'):
                        copy_count += 1
                        file_real_path = os.path.join(file_path, file_name)
                        # 复制文件
                        shutil.copy(file_real_path, dst_path)
                        # print(dst_path)
                        if copy_count == spe_num:
                            break
    
    print('C- special num: {} patient num: {}'.format(spe_num, threshold_count))
    # N
    threshold_count = 0
    for one_name in n_lists:
        file_path = os.path.join(n_path, one_name)
        file_lists = os.listdir(file_path)
        k_position = -1
        n_nodules_count = 0
        # 判断帧数是否足够
        for idx, file_name in enumerate(file_lists):
            if file_name.endswith('k.jpg'):
                k_position = idx
            if file_name.startswith('N'):
                n_nodules_count += 1

        copy_count = 0

        if n_nodules_count >= spe_num:
            if threshold_count == patient_num_threshold:
                break
            threshold_count += 1
            
            # create save_path
            dst_path = os.path.join(save_path, 'N/' + one_name)
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            # z_position detection
            z_position = -1
            for idx, file_name in enumerate(file_lists):
                if file_name.startswith('Z'):
                    z_position = idx

            len_lists = len(file_lists)
            file_name = file_lists[k_position]
            file_real_path = os.path.join(file_path, file_name)
            # 复制关键帧
            shutil.copy(file_real_path, dst_path)
            copy_count += 1
            if copy_count == spe_num:
                print('task finished.')
                exit(0)
            # print(dst_path)
            
            # left & right
            for idx_ in range(1, len_lists):
                if k_position - idx_ >= 0:
                    # left
                    file_name = file_lists[k_position-idx_]
                    if file_name.startswith('N'):
                        copy_count += 1
                        file_real_path = os.path.join(file_path, file_name)
                        # 复制文件
                        shutil.copy(file_real_path, dst_path)
                        # print(dst_path)
                        if copy_count == spe_num:
                            break

                # right
                if k_position + idx_ < z_position:
                    file_name = file_lists[k_position+idx_]
                    if file_name.startswith('N'):
                        copy_count += 1
                        file_real_path = os.path.join(file_path, file_name)
                        # 复制文件
                        shutil.copy(file_real_path, dst_path)
                        # print(dst_path)
                        if copy_count == spe_num:
                            break
    print('N- special num: {} patient num: {}'.format(spe_num, threshold_count))
    