# import os
# import glob
# 
# fm_lists = glob.glob('/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification/*/*/*//*.fm.npy')
# print(fm_lists)
import os

end_name = '.fm.npy'
# end_name = '_key.jpg'
# 从指定path下递归获取所有文件
def getAllFile(path, fileList):
    dirList = []    # 存放文件夹路径的列表
    for ff in os.listdir(path):
        wholepath = os.path.join(path, ff)
        if os.path.isdir(wholepath):
            dirList.append(wholepath)   # 如果是文件添加到结果文件列表中

        if os.path.isfile(wholepath):
            if wholepath.endswith(end_name):
                fileList.append(wholepath)  # 如果是文件夹，存到文件夹列表中

    for dir in dirList:
        getAllFile(dir, fileList)   # 对于dirList列表中的文件夹，递归提取其中的文件，fileList一直在往下传，所有的文件路径都会被保存在这个列表中

if __name__ == '__main__':
    flist = []
    findpath = '/media/oem/sda21/cxx/breast_all/Video/All_Test_To_Pure_By_Nodules_Model_copy/'
    getAllFile(findpath, flist)
    print('Docfile:', len(flist))	# filepath下的指定文件总数（这里是.doc文件的数量）
    for ff in flist:
        print(ff)
        os.remove(ff) 