# improved by Abner  2021-05-14 For extract the C/N/H frame. 
# CUDA_VISIBLE_DEVICES=2 python 1.breast_mix_extract_frame.py
from posixpath import commonpath
from turtle import begin_poly
import xlrd
import os
import imageio
from imageio import imread, imsave
import re
import numpy as np
import shutil

'''
    Path setting.
'''
patient_type = '恶性' # 恶性 良性
excel_type = 4 # 4:视频标记1-116.xlsx  or  1: 视频标记-117号之后.xlsx

#### excel-117号之后的良性仅仅到了384，而不是500 ###

year_ = '2021'
base_path = '/media/oem/sda21/cxx/breast_all/Video'
save_path = base_path + '/for_thesis/original/2022_All_C_Nodules_Original'
csv_path = base_path + '/结节帧位excel/视频标记1-116.xlsx' # 视频标记-117号之后.xlsx   视频标记1-116.xlsx
path = base_path + '/视频/C'
## end settig
# ===============================================================================
error_file_name = 'ty_' + str(excel_type) + '_' + patient_type + '_' + year_
error_count = 0
f_err = open(error_file_name, 'a')
def get_path(path):
    file = os.listdir(path)
    for i in file:
        print("i:", i)

def save_health_frame(i, begin_pos, end_pos, all_img, file_name_, sheet2_):
    if begin_pos == -1:
        begin_ = 0
    else:
        begin_ = sheet2_.cell_value(i, begin_pos)
        if begin_ != '':
            begin_ = int(begin_)
        else:
            return False
    
    end_ = sheet2_.cell_value(i, end_pos)
    if begin_ == '' or end_ == '':
        return False
    else:
        end_ = int(end_)

    for k in range(begin_, end_):
        imgname = file_name_ + "/" + "Z" + f"{k}" + ".jpg"
        imsave(imgname, all_img[k])
    return True

def save_img(i, sheet2, all_img, file_name, img_name, lens):
    if patient_type == '恶性':
        patient_type_ = 'C'
    if patient_type == '良性':
        patient_type_ = 'N'

    global error_count
    '''Notes: Extract key frame
    '''
    if excel_type == 4:
        key = 6
    elif excel_type == 1:
        key = 5
    
    flag = len(str(sheet2.cell_value(i, key))) > 0
    while flag:
        try:
            k = int(sheet2.cell_value(i, key))
            imgname = file_name +"/"+ patient_type_ + f"{k}"+"_k" + ".jpg"
            imsave(imgname, all_img[k])
            key = key + 3
            flag = len(str(sheet2.cell_value(i, key))) > 0
        except:
            break
    ## endl /key
    
    '''
        Notes: Extract health frame
        针对健康帧：需要加入表格数据为空判断 & 自动计算列数 2022-02-19 @Abner
        针对结节帧：仅仅取第一个三元组数据，后面有的话暂时不考虑要了。
    '''
    ## endl / key frame
    # positon in the table, maybe some difference.
    first = -1 # stand for no valid index. There are instructions in the function of `avi_nums`.
    one_intervals_flag = 0

    # 4:视频标记1-116.xlsx  or  1: 视频标记-117号之后.xlsx
    # internal rows: 4
    
    begin_flag = 1
    return_value = True
    if excel_type == 4:
        next_inter_1 = 1
        next_inter_2 = 2
    elif excel_type == 1:
        next_inter_1 = 2
        next_inter_2 = 1
    
    interval_begin = 4
    end_pos = interval_begin
    begin_1 = sheet2.cell_value(i, interval_begin)
    too_length_flag = 0 # e.g. 良性112号太长了。
    if begin_1 != '':
        begin_1 = int(begin_1)
    else:
        begin_1 = -1

    if begin_1 > 1:
        begin_pos = -1
    else:
        # 计算结束帧
        interval_end = interval_begin + next_inter_1
        begin_pos = interval_end
        # 计算下一个起始位置帧
        next_interval_begin = interval_end + next_inter_2
        end_pos = next_interval_begin

    while(True):
        try:
            if not save_health_frame(i, begin_pos, end_pos, all_img, file_name, sheet2):
                break
        except:
            too_length_flag = 1
            break
        # 更新
        interval_begin = end_pos
        # 计算结束帧
        interval_end = interval_begin + next_inter_1
        begin_pos = interval_end
        # 计算下一个起始位置帧
        next_interval_begin = interval_end + next_inter_2
        end_pos = next_interval_begin

    if not too_length_flag:
        end_confirm = sheet2.cell_value(i, end_pos)
        new_begin_value = sheet2.cell_value(i, interval_end)
        if new_begin_value != '':
            new_begin_value = int(new_begin_value)
            if end_confirm == '' and new_begin_value < len(all_img)-1:
                for k in range(new_begin_value, len(all_img)-1):
                    imgname = file_name + "/" + "Z" + f"{k}" + ".jpg"
                    imsave(imgname, all_img[k])

    '''
        Notes: Extract nudules frame
    '''
    next_add = 3
    if excel_type == 4:
        first = 4
        end = 5
    elif excel_type == 1:
        first = 4
        end = 6
    
    flag = len(str(sheet2.cell_value(i, first))) > 0
    try:
        first_value = int(sheet2.cell_value(i, first))
        end_value = int(sheet2.cell_value(i, end))
        nums = avi_nums(i, first, end, sheet2)

        # first_value += nums
        # end_value -= nums

        while (flag):
            for k in range(first_value, end_value):
                if (k - first_value) % nums == 0:
                    imgname = file_name +"/"+patient_type_ + f"{k}" + ".jpg"
                    imsave(imgname, all_img[k])
                else:
                    continue
            # 根据excel下一个起始数据距上一个3
            first = first + next_add
            end = end + next_add
            first_value = int(sheet2.cell_value(i, first))
            end_value = int(sheet2.cell_value(i, end))
            flag = len(str(sheet2.cell_value(i, first))) > 0
            nums = avi_nums(i, first, end, sheet2)
    except:
        pass
    
    ## endl /nodules
    save_all_img = os.listdir(file_name)
    nudules_flag = 0
    health_flag = 0
    key_flag = 0

    for img_ in save_all_img:
        if img_[0] == 'C' or img_[0] == 'N':
            nudules_flag = 1
        if img_[0] == 'Z':
            health_flag = 1
        if img_.endswith('_k.jpg'):
            key_flag = 1
        if key_flag + health_flag + nudules_flag== 3:
            break

    if key_flag + health_flag + nudules_flag != 3:
        shutil.rmtree(file_name)
        f_err.write('no save {}\n'.format(sheet2.cell_value(i, 0)))
        error_count +=1
        print('error num: {} len(all_img):{}'.format(sheet2.cell_value(i, 0), len(all_img)))

def red_excel(path,sheet2):
    files = os.listdir(path)
    # 读取所有视频的名称list,
    for i, file in enumerate(files):
        img_name = re.search("[0-9]+", file).group()
        file_name = save_path + "/"+img_name
        rpath = path +"/" + file
        

        # 4:视频标记1-116.xlsx  or  1: 视频标记-117号之后.xlsx
        if excel_type == 4:
            # interval 4
            x = (int(img_name) - 1) * 4 + 1 # excel 从0行开始的
            if x > 461:
                continue

        elif excel_type == 1:
            # interval 1
            # 117号之后的良性仅仅到了387， max -> 276， 55, 221
            x = int(img_name) - 116
            if patient_type == '良性':
                if x > 271 or x <= 0:
                    continue

            elif patient_type == '恶性':
                if x > 384 or x <= 0:
                    continue
        
        if (not (os.path.exists(file_name))):
            os.makedirs(file_name)

        all_img, lens = red_avi(rpath)
        print('[{}/{}] {}'.format(i, len(files), file))
        save_img(x, sheet2, all_img, file_name, img_name, lens)

def red_avi(rpath):
    avidata = imageio.get_reader(rpath)
    all_img = []
    all_img.clear()
    for cc, img in enumerate(avidata):
        all_img.append(img)
    all_img_lens = len(all_img)
    # nums = avi_nums(all_img_lens)
    return all_img, all_img_lens

def avi_nums(i, first, end, sheet2, first_value=None):
    # 通过判断一段视频间的帧数距离，来设置提取的间隔
	# Sheet.cell_value(row, column, new_value=None)
    if first_value == None:
        if first!=-1:
                first_value = int(sheet2.cell_value(i, first))
        else:
            first_value = 0

    if sheet2.cell_value(i, end)=='':
        print('next intervals not exists.')
        return -1

    end_value = int(sheet2.cell_value(i, end))
    lens = np.abs(end_value - first_value)
    
    return 1

def main():
    x1 = xlrd.open_workbook(csv_path)
    sheet2 = x1.sheet_by_name(patient_type)
    red_excel(path, sheet2)

if __name__ == '__main__':
    main()
    print('final error count: ',error_count)