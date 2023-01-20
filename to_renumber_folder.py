# /home/qianxianserver/data/cxx/breast_all/breast/20210611_体检乳腺数据/BR_three_class
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
            # print(dstname)
            shutil.copy2(srcname, dst)


ind = 0
save_path = '/home/qianxianserver/data/cxx/breast_all/breast/20210611_体检乳腺数据/N_All/'
save_pure_nodules_path = '/home/qianxianserver/data/cxx/breast_all/breast/20210611_体检乳腺数据/N_Nodules_pure_all/'
save_pure_health_path = '/home/qianxianserver/data/cxx/breast_all/breast/20210611_体检乳腺数据/Health_all/'

def iterate_handle(path):
    global ind
    for root, dirs, _ in os.walk(path):
        if len(dirs)==0:
            return False

        for dir in dirs:
            new_path = os.path.join(root, dir)
            if not iterate_handle(new_path):
                # add folder
                if not os.path.exists(save_path + str(ind)):
                    os.makedirs(save_path + str(ind))

                dir_copyTree(new_path, save_path + str(ind))
                
                lists_folders = os.listdir(new_path)
                k_flag = 0
                n_flag = 0
                h_flag = 0
                for name_ in lists_folders:
                    if name_[0] == 'Z':
                        h_flag = 1
                        if not os.path.exists(save_pure_health_path + str(ind)):
                            os.makedirs(save_pure_health_path + str(ind))

                        shutil.copy(new_path + '/' + name_,save_pure_health_path  + str(ind) + '/' + name_)

                    else:
                        if name_.endswith('k.jpg'):
                            k_flag = 1
                        if name_[0] == 'N':
                            n_flag = 1

                        if not os.path.exists(save_pure_nodules_path + str(ind)):
                            os.makedirs(save_pure_nodules_path + str(ind))

                        shutil.copy(new_path + '/' + name_, save_pure_nodules_path  + str(ind) + '/' + name_)

                if k_flag + n_flag + h_flag != 3:
                    print('err: ', new_path)

                ind += 1
        return True

def main():
    path = '/home/qianxianserver/data/cxx/breast_all/breast/20210611_体检乳腺数据/BR_three_class/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    else:
        shutil.rmtree(save_path)

    iterate_handle(path)


if __name__ == '__main__':
    main()
