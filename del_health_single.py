import os
base_path_n = '/home/qianxianserver/data/cxx/breast_all/breast/20210611_体检乳腺数据/Health_all/'

n_h_lists = os.listdir(base_path_n)
max_frame_num = 5
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

sum_del = 0

for th in n_h_lists: # del 5000
    th_ = base_path_n + th
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
                        full_name1 = base_path_n + th + '/' + i
                        os.remove(full_name1)
                        del_num_count += 1

            for del_ in del_list:
                th_1.remove(del_)
            del_list.clear()  

            # stop died circle
            if del_num_count == 0:
                del_num_count = 1
            file_num -= del_num_count