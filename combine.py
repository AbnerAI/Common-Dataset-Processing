import os
import shutil

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

base_path_c = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/Combine/C'
base_path_n = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/Combine/N'

another_c = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/Combine/All_C_Crop'
another_n = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/Combine/All_N_Crop'
import glob
for i in os.listdir(base_path_n):
    for j in os.listdir(another_n):
        if i==j:
            cop = another_n + '/' + j
            jpg_lists = glob.glob(cop + '/*.jpg')
            for itm in jpg_lists:
                shutil.copy(itm, base_path_n + '/' + i)
