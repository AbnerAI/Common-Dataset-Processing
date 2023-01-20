import os
root = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk3_K/'
base_path_c = root + 'C/'
base_path_n = root + 'N/'

c_h_lists = os.listdir(base_path_c)
n_h_lists = os.listdir(base_path_n)
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

for th in c_h_lists: # del 5000
    th_ = root + 'C/' + th
    th_1 = os.listdir(th_)

    # statistic health frame number
    file_num = 0
    for g_h in th_1:
        if g_h[0]=='Z':
            file_num += 1
     
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
                    if i[0]=='Z':
                        del_list.append(i)
                        full_name1 = root + 'C/' + th + '/' + i
                        os.remove(full_name1)
                        del_num_count += 1

            for del_ in del_list:
                th_1.remove(del_)
            del_list.clear()
                    
            # stop died circle
            if del_num_count == 0:
                del_num_count = 1
            file_num -= del_num_count

print(sum_del)

sum_del = 0

for th in n_h_lists: # del 5000
    th_ = root + 'N/' + th
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
                    if i[0]=='Z':
                        del_list.append(i)
                        full_name1 = root + 'N/' + th + '/' + i
                        os.remove(full_name1)
                        del_num_count += 1

            for del_ in del_list:
                th_1.remove(del_)
            del_list.clear()  

            # stop died circle
            if del_num_count == 0:
                del_num_count = 1
            file_num -= del_num_count