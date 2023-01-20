import os
import glob
import shutil
import numpy as np
import glob

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

def main():
    # output = '/home/qianxianserver/data/cxx/ultrasound_data/勾画图片及json/Data/Lists'
    # path = '/home/qianxianserver/data/cxx/ultrasound_data/勾画图片及json/Data'




    output = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk2/Mix_Data/New/Train'
    path = output

    if not os.path.exists(output):
        os.mkdir(output)
    
    txtName = './mix_to_pure_lists_train_breast_all.txt'
    f=open(txtName, "a+")

    file_list_c = os.listdir(path + '/C') #.代表根目录下
    file_list_n = os.listdir(path + '/N') #.代表根目录下

    for item_c in file_list_c:
        print(path + '/C/' +item_c)
        if len(os.listdir(path + '/C/' +item_c))!=0:
            listing = os.listdir(path + '/C/' +item_c)
            for files in listing:
                if files.endswith('.jpg'):
                    f.write(path + '/C/' +item_c + ' C' + '\n')
                    break
        
    for item_n in file_list_n:
        print(path + '/N/' +item_n)
        if len(os.listdir(path + '/N/' +item_n))!=0:
            listing = os.listdir(path + '/N/' +item_n)
            for files in listing:
                if files.endswith('.jpg'):
                    f.write(path + '/N/' +item_n + ' N' + '\n')
                    break
    
    f.close()
    
if __name__ == "__main__":
    main()




# import os
# count = 0

# # 遍历文件夹
# def walkFile(file):
#     for root, dirs, files in os.walk(file):
#         # root 表示当前正在访问的文件夹路径
#         # dirs 表示该文件夹下的子目录名list
#         # files 表示该文件夹下的文件list
        
#         # 遍历文件
#         for f in files:
#             global count
#             count += 1
#             print(os.path.join(root, f))

#         # 遍历所有的文件夹
#         for d in dirs:
#             print(os.path.join(root, d))
#     print("文件数量一共为:", count)

# if __name__ == '__main__':
#     walkFile(r"/home/qianxianserver/data/cxx/ultrasound/TJDataClassification/TJ_H")