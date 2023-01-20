# improved by Abner  2021-11-27 For extract the C/N/H frame and remain all frame of patient partly 
# CUDA_VISIBLE_DEVICES=2 python N1.breast_mix_extract_frame_for_all_frame.py
import re
import os
import xlrd
import shutil
import imageio
import numpy as np
from imageio import imread, imsave

'''
    Path setting.
'''
patient_type = '良性' # 恶性 良性
excel_type = 4 # 4:视频标记1-116.xlsx  or  1: 视频标记-117号之后.xlsx

# 2021
year_ = '2021'
base_path = '/media/oem/sda21/cxx/breast_all/Video'
save_path = base_path + '/All_N_Test'
csv_path = base_path + '/结节帧位excel/视频标记1-116.xlsx' # 视频标记-117号之后.xlsx   视频标记1-116.xlsx
path = base_path + '/视频/N'
## end settig
# ===============================================================================
error_file_name = 'ty_' + str(excel_type) + '_' + patient_type + '_' + year_
error_count = 0
f_err = open(error_file_name, 'a')
def get_path(path):
    file = os.listdir(path)
    for i in file:
        print("i:", i)

def save_img(i, sheet2, all_img, file_name, img_name, lens):
    if patient_type == '恶性':
        patient_type_ = 'C'
    if patient_type == '良性':
        patient_type_ = 'N'

    # Extract all frame


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
    '''
    ## endl / key frame
    # positon in the table, maybe some difference.
    first = -1 # stand for no valid index. There are instructions in the function of `avi_nums`.
    one_intervals_flag = 0
    # internal rows: 4
    if excel_type == 4:
        interval_lists = [4, 5, 7, 8, 10, 11, 13]
    elif excel_type == 1: 
        # internal rows: 1
        interval_lists = [4, 6, 7, 9, 10, 12, 13]
    # flag = len(str(sheet2.cell_value(i, first))) > 0

    try:
        # print('first {} end {}'.format(first, interval_lists[0]))
        nums = avi_nums(i, first, interval_lists[0], sheet2)
        if nums!=-1:
            # print('cur nums: ', nums)
            end_ = int(sheet2.cell_value(i, interval_lists[0]) - 5)
            for k in range(0, end_):
                # print("开始：{},结束:{}".format(3, end_))
                if k % nums == 0:
                    imgname = file_name + "/" + "Z" + f"{k}" + ".jpg"
                    
                    imsave(imgname, all_img[k])

    except:
        pass
    try:
        end_ = int(sheet2.cell_value(i, interval_lists[2]) - 5)
        first_ = int(sheet2.cell_value(i, interval_lists[1]) + 5)
        nums = avi_nums(i, interval_lists[1], interval_lists[2], sheet2)
        if nums!=-1:
            for k in range(first_, end_):
                if (k - first_) % 2 == 0:
                    imgname = file_name + "/" + "Z" + f"{k}" + ".jpg"
                    imsave(imgname, all_img[k])
    except:
        one_intervals_flag += 1

    
    try:
        first_ = int(sheet2.cell_value(i, interval_lists[3]) - 5)
        end_ = int(sheet2.cell_value(i, interval_lists[4]) + 5)
        # print('first {} end {}'.format(interval_lists[3],interval_lists[4]))
        nums = avi_nums(i, interval_lists[3], interval_lists[4], sheet2)
        if nums!=-1:
            for k in range(first_, end_):
                # print("开始：{},结束:{}".format(3, first_))
                # 必须取关键帧，然后每隔2帧取一帧
                if (k - first_) % nums == 0:
                    imgname = file_name + "/" + "Z" + f"{k}" + ".jpg"
            
                    imsave(imgname, all_img[k])
                    # print("成功保存：", k)
    except:
        one_intervals_flag += 1
        
    try:
        first_ = int(sheet2.cell_value(i, interval_lists[5]) - 5)
        end_ = int(sheet2.cell_value(i, interval_lists[6]) + 5)
        # print('first {} end {}'.format(interval_lists[5],interval_lists[6]))
        nums = avi_nums(i, interval_lists[5], interval_lists[6], sheet2)
        if nums!=-1:
            for k in range(first_, end_):
                # print("开始：{},结束:{}".format(3, first_))
                # 必须取关键帧，然后每隔2帧取一帧
                if (k - first_) % nums == 0:
                    imgname = file_name + "/" + "Z" + f"{k}" + ".jpg"
                    # print(imgname)
                    imsave(imgname, all_img[k])
    except:
        one_intervals_flag += 1
    
    if one_intervals_flag>=3:
        first = -2
        if excel_type == 4:
            right_to_end = interval_lists[0] + 1 
        else:
            right_to_end = interval_lists[0] + 2 

        nums = avi_nums(i, first, right_to_end, sheet2, first_value=len(all_img))
        if nums!=-1:
            end_ = int(sheet2.cell_value(i, right_to_end)) + 4
            for k in range(end_, len(all_img)-1):
                if (k-end_) % nums == 0:
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
        first_value = int(sheet2.cell_value(i, first) + 4)
        end_value = int(sheet2.cell_value(i, end) -4)
        nums = avi_nums(i, first, end, sheet2)
        nums = 2 # fixed

        first_value += nums
        end_value -= nums

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
            first_value = int(sheet2.cell_value(i, first) + 4)
            end_value = int(sheet2.cell_value(i, end) - 4)
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
    # 读取所有视频的名称list
    # 这块的算法效率有点低，暂时这样吧。
    for i, file in enumerate(files):
        # 从视频文件的名称中提取img_name
        img_name = re.search("[0-9]+", file).group()
        file_name = save_path + "/"+img_name
        rpath = path +"/" + file
        
        # interval 4: 1~116
        if excel_type == 4:
            x = (int(img_name) - 1) * 4 + 1
            # if x > 465: # Train: 465->373(465-116*0.2*4), Test: 373->465 . Modify by abner 2021-11-27 
            if x <= 373 or x > 465: # Train: 465->373(465-116*0.2*4), Test: 373->465 . Modify by abner 2021-11-27 
                continue
            
        elif excel_type == 1:
        # interval 1: number of patient: 384
            x = int(img_name) - 116 
            # if x > 386 or x <= 0: # Test: 386->463(386 + 77), Train: 463+(463 + 307) . Modify by abner 2021-11-27 
            if patient_type == '良性':
                if x <= 221 or x>276:
                    continue
            elif patient_type == '恶性':
                if x <= 310 or x>386: # Test: 386->310(386 - 76), Train: 463+(463 + 307) . Modify by abner 2021-11-27 
                    continue
        
        if (not (os.path.exists(file_name))):
            os.makedirs(file_name)

        all_img, lens = red_avi(rpath)
        print('[{}/{}] {}'.format(i, len(files), file))
        # save all_img directly
        for j in range(lens):
            imsave(file_name + '/' + str(j) + '.jpg', all_img[j])

        # save_img(x, sheet2, all_img, file_name, img_name, lens)

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
                first_value = int(sheet2.cell_value(i, first)) + 2
        else:
            first_value = 0

    if sheet2.cell_value(i, end)=='':
        print('next intervals not exists.')
        return -1

    end_value = int(sheet2.cell_value(i, end) - 2)
    lens = np.abs(end_value - first_value)
    
    return lens//20

def main():
    x1 = xlrd.open_workbook(csv_path)
    sheet2 = x1.sheet_by_name(patient_type)
    red_excel(path, sheet2)

if __name__ == '__main__':
    main()
    print('final error count: ',error_count)