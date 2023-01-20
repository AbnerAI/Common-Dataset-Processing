# form new dataset, three
# funciton: 
import os
import glob
import shutil

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
            # print(dstname)
            shutil.copy2(srcname, dst)

# C
# base_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/All_Crop_zk_Del_Repeat/C'
# output_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk2/C'
# flag_ = '_c'
# flag_1 = '/C/'

# N
base_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/All_Crop_zk_Del_Repeat/N'
output_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk2/N'
flag_ = '_n'
flag_1 = '/N/'


output_z_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk2/H'
output_pure_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk2/Pure'


# # C
# base_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk3_K/C'
# output_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk3_K/test/C'
# flag_ = '_c'
# flag_1 = '/C/'
# # 

# # N
# # base_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk3_K/N'
# # output_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk3_K/test/N'
# # flag_ = '_n'
# # flag_1 = '/N/'


# output_z_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk3_K/test/H'
# output_pure_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk3_K/Pure'

if not os.path.exists(output_path):
    os.mkdir(output_path)
if not os.path.exists(output_z_path):
    os.mkdir(output_z_path)
if not os.path.exists(output_pure_path):
    os.mkdir(output_pure_path)
    os.mkdir(output_pure_path + '/C')
    os.mkdir(output_pure_path + '/N')

# /home/qianxianserver/data/cxx/breast_all/breast
if __name__ == '__main__':
    lists = os.listdir(base_path)
    for item in lists:
        file_all = os.listdir(base_path + '/' + item)
        exist_flag = 0
        for name in file_all:
            if name[0]=='Z' and name[1].isdigit():
                exist_flag = 1
                if not os.path.exists(output_z_path + '/' + item + flag_):
                    os.mkdir(output_z_path + '/' + item + flag_)
                shutil.copy(base_path + '/' + item + '/' + name, output_z_path + '/' + item + flag_ + '/' + name)
            
        if exist_flag:
            print(base_path + '/' + item)
            if not os.path.exists(output_path + '/' + item):
                os.mkdir(output_path + '/' + item)
            dir_copyTree(base_path + '/' + item, output_path + '/' + item)
            
            # pure data
            for name in file_all:
                # if name[0]=='C' or name[0]=='N':
                if not (name[0]=='Z' and name[1].isdigit()):
                    if not os.path.exists(output_pure_path + flag_1 + item + flag_):
                        os.mkdir(output_pure_path + flag_1 + item + flag_)
                    shutil.copy(base_path + '/' + item + '/' + name, output_pure_path + flag_1 + item + flag_ + '/' + name)