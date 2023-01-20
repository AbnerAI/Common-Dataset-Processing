import os
import glob
import shutil
import numpy as np
import pandas as pd
from random import shuffle

# 目录递归拷贝函数
def dir_copyTree(src, dst):
  names = os.listdir(src)
  # 目标文件夹不存在，则新建
  if not os.path.exists(dst):
    os.mkdir(dst)
  # 遍历源文件夹中的文件与文件夹
  for name in names:
    srcname = os.path.join(src, name)
    dstname = os.path.join(dst, name)
    # 是文件夹则递归调用本拷贝函数，否则直接拷贝文件
    if os.path.isdir(srcname):
        dir_copyTree(srcname, dstname)
    else:
        if (not os.path.exists(dstname)
            or ((os.path.exists(dstname))
            and (os.path.getsize(dstname) != os.path.getsize(srcname)))):
            print(dstname)
            shutil.copy2(srcname, dst)

def generate_lists(output, path, txtName):
    f=open(txtName, "a+")

    file_list_c = os.listdir(path + '/C') #.代表根目录下
    file_list_n = os.listdir(path + '/N') #.代表根目录下

    for item_c in file_list_c:
        # print(path + '/C/' +item_c)
        if len(os.listdir(path + '/C/' +item_c))!=0:
            listing = os.listdir(path + '/C/' +item_c)
            for files in listing:
                if files.endswith('_key.jpg'):
                    f.write(path + '/C/' +item_c + ' C' + '\n')
                    break
   
    for item_n in file_list_n:
        # print(path + '/N/' +item_n)
        if len(os.listdir(path + '/N/' +item_n))!=0:
            listing = os.listdir(path + '/N/' +item_n)
            for files in listing:
                if files.endswith('_key.jpg'):
                    f.write(path + '/N/' +item_n + ' N' + '\n')
                    break
    f.close()



# show statistic & divide
# classification datasets divide: root->C   root->N
# root = '/home/qianxianserver/data/cxx/ultrasound20210312FinalTwoClassification/ultrasound/6-get_hy_key_frame/all_tj_data_have_key_frame/'
root = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/C_N_0524'

c_path = os.listdir(os.path.join(root, 'C'))
n_path = os.listdir(os.path.join(root, 'N'))
# h_path = os.listdir(os.path.join(root, 'H'))

print('[ALL] C_Len {}, N_Len {}, Por {}'.format(len(c_path), len(n_path), len(c_path)/len(n_path)))
# 7:3
train_c_len = int(len(c_path) * 0.7)  
train_n_len = int(len(n_path) * 0.7)
# train_h_len = int(len(h_path) * 0.7)

eval_c_len = len(c_path) - train_c_len
eval_n_len = len(n_path) - train_n_len
# eval_h_len = len(h_path) - train_h_len

print('[Divide] train_c_len {}, train_n_len {}, eval_c_len {} eval_n_len {}'.format(train_c_len, train_n_len, eval_c_len, eval_n_len))

# get train & eval lists
if not os.path.exists(root + '/New'):
    os.mkdir(root + '/New')    
    os.mkdir(root + '/New/Train')    
    os.mkdir(root + '/New/Train/C')    
    os.mkdir(root + '/New/Train/N')    
    os.mkdir(root + '/New/Test')    
    os.mkdir(root + '/New/Test/C')    
    os.mkdir(root + '/New/Test/N')    
    
    shuffle(c_path)
    shuffle(n_path)
    # shuffle(h_path)

    new_train_c_path = c_path[:train_c_len]
    new_train_n_path = n_path[:train_n_len]
    # new_train_h_path = h_path[:train_h_len]

    new_test_c_path = c_path[train_c_len:]
    new_test_n_path = n_path[train_n_len:]
    # new_test_h_path = h_path[train_h_len:]

    # copy new data to new path
    for item_c in new_test_c_path:
        dir_copyTree(root + '/C/' + item_c, root + '/New/Test/C/' + item_c)
        
    for item_n in new_test_n_path:
        dir_copyTree(root + '/N/' + item_n, root + '/New/Test/N/' + item_n)

    for item_c in new_train_c_path:
        dir_copyTree(root + '/C/' + item_c, root + '/New/Train/C/' + item_c)

    for item_n in new_train_n_path:
        dir_copyTree(root + '/N/' + item_n, root + '/New/Train/N/' + item_n)

else:
    # generate lists
    output = root + '/New/Train/Lists'
    path = root + '/New/Train'
    if not os.path.exists(output):
        os.mkdir(output)
    txtName = output + '/lists_train.txt'
    generate_lists(output, path, txtName)

    output = root + '/New/Test/Lists'
    path = root + '/New/Test'
    if not os.path.exists(output):
        os.mkdir(output)
    txtName = output + '/lists_eval.txt'
    generate_lists(output, path, txtName)