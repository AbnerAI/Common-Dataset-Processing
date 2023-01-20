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

# original_c = os.listdir('/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/All_C')
# original_n = os.listdir('/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/All_N')
base_path_c = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/All_C_Crop/'
base_path_n = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/All_N_Crop/'

save_base_path = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/'

file_c = open('./good_names/new_lists_c_348.txt')
file_n = open('./good_names/new_lists_n_340.txt')

if not os.path.exists(save_base_path + 'save/c'):
    os.makedirs(save_base_path + 'save/c')
    os.makedirs(save_base_path + 'save/n')

while True:
    line = file_c.readline().replace('\n','')
    if not line:
        break
    try:
        dir_copyTree(base_path_c + line, save_base_path + 'save/c/' + line)
    except:
        pass

while True:
    line = file_n.readline().replace('\n','')
    if not line:
        break
    try:
        dir_copyTree(base_path_n + line, save_base_path + 'save/n/'  + line)
    except:
        pass