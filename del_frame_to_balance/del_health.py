import os
# /home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification/Pure/New/Test/H
# /home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification/Pure/New/Train/H
root = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk2/'
base_path_test = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk2/Pure/New/Test/H'
base_path_train = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk2/Pure/New/Train/H'
test_h_lists = os.listdir(base_path_test)
train_h_lists = os.listdir(base_path_train)
max_frame_num = 13
sum_del = 0

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
    th_ = base_path_test + '/' + th
    th_1 = os.listdir(th_)
    file_num = len(th_1)
    while True:        
        del_num = get_del_num(file_num, max_frame_num)
        if del_num==-1:
            break
        else:
            del_num_count = 0
            del_list = list()
            for index, i in enumerate(th_1):
                print(index)
                if index%del_num==0:
                    del_list.append(i)
                    # del Pure/New/Test/h
                    full_name1 = root + 'Pure/New/Test/H/' + th + '/' + i

                    os.remove(full_name1)

                    # del Mix_Data/New/Test/h
                    full_name2 = root + 'Mix_Data/New/Test/H/' + th + '/' + i
                    os.remove(full_name2)
                    
                    # del Mix_Data/New/Test/c h
                    try:
                        full_name3 = root + 'Mix_Data/New/Test/C/' + th[:-2] + '/' + i
                        os.remove(full_name3)
                    except:
                        # del Mix_Data/New/Test/n h 
                        full_name4 = root + 'Mix_Data/New/Test/N/' + th[:-2] + '/' + i
                        os.remove(full_name4)
                    del_num_count += 1
            for del_ in del_list:
                th_1.remove(del_)
            del_list.clear()
                    
            file_num -= del_num_count


print(sum_del)

# max_frame_num = 15
sum_del = 0

for th in train_h_lists: # del 5000
    th_ = base_path_train + '/' + th
    th_1 = os.listdir(th_)
    file_num = len(th_1)
    while True:        
        del_num = get_del_num(file_num, max_frame_num)
        if del_num==-1:
            break
        else:
            del_num_count = 0
            del_list = list()
            for index, i in enumerate(th_1):
                print(index)
                if index%del_num==0:
                    # del Pure/New/Train/h
                    del_list.append(i)

                    full_name1 = root + 'Pure/New/Train/H/' + th + '/' + i
                    os.remove(full_name1)

                    # del Mix_Data/New/Train/h
                    full_name2 = root + 'Mix_Data/New/Train/H/' + th + '/' + i
                    os.remove(full_name2)
                    try:
                        # del Mix_Data/New/Train/c h
                        full_name3 = root + 'Mix_Data/New/Train/C/' + th[:-2] + '/' + i
                        os.remove(full_name3)
                    except:
                        # del Mix_Data/New/Train/n h 
                        full_name4 = root + 'Mix_Data/New/Train/N/' + th[:-2] + '/' + i
                        os.remove(full_name4)
                    del_num_count += 1
            for del_ in del_list:
                th_1.remove(del_)
            del_list.clear()  

            file_num -= del_num_count