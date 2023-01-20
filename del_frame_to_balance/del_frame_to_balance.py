import os
import numpy as np
base_path = '/media/oem/sda21/cxx/breast_all/Video/All_N_Train_Crop_Copy/'
test_h_lists = os.listdir(base_path)
max_frame_num = 35
sum_del = 0
del_char = 'Z'

# find All_C_Train_Crop_Copy/  -type f -name “C*” | wc -l
def get_del_num(file_num, max_frame_num):
    if file_num > max_frame_num:
        del_num = file_num - max_frame_num
        # sum_del += del_num
        if file_num%del_num==0:
            p = (file_num//del_num) 
        else:
            p = (file_num//del_num) + 1
        return p
    else:
        return -1
        
for th in test_h_lists: # del 5000
    th_ = base_path + '/' + th
    th_1 = np.array(os.listdir(th_))
    print(th_1)
    # file_num = len(th_1)
    file_num = len(th_1[np.char.count(th_1, del_char, start=0, end=None)!=0])
    while True:        
        del_num = get_del_num(file_num, max_frame_num)
        if del_num==-1:
            break
        else: 
            del_num_count = 0
            del_list = list()
            idx = 0
            for i in th_1:
                if i[0] == del_char:
                    idx += 1
                    if idx%del_num==0:
                        del_list.append(i)
                        full_name1 = base_path + th + '/' + i
                        os.remove(full_name1)
                        del_num_count += 1
            
            th_1 = th_1.tolist()
            
            for del_ in del_list:
                th_1.remove(del_)
            del_list.clear()
            
            th_1 = np.array(th_1)
            file_num -= del_num_count

print(sum_del)