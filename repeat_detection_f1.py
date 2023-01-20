# 去重
import cv2
import os
import shutil
import numpy as np

def main(type_):
    img_path = "/media/oem/sda21/cxx/breast_all/Video/All_Test_To_Pure_By_Nodules_Model_copy/"
    save_path = "/media/oem/sda21/cxx/breast_all/Video/All_Test_To_Pure_By_Nodules_Model_copy_del_repeat/"
    threshold = 0.55 # <threshold, will be save.   me: N: 0.6 3423   C:0.53 4200+  zk: N: 0.63 3417    C: 0.55 4126
    
    img_c = img_path + type_ + '/'
    save_path = save_path + type_ + '/'
    img_dir = os.listdir(img_c)
    record = []
    for i, name in enumerate(img_dir):
        name = '97'

        simg_name = img_c+name+"/"
        ssave_name = save_path+name+"/"
        print(simg_name)
        timg_name = os.listdir(simg_name)
        ssave_name_list = os.listdir(ssave_name)
        flag_ = 0
        for j, sname in enumerate(timg_name):
            fimg_name = simg_name+sname
            record = []
            record.clear()
            if not flag_:
                for k, tname in enumerate(ssave_name_list):
                    finasave_img = simg_name+tname
                    name1 = fimg_name
                    name2 = finasave_img
                    img1 = cv2.imdecode(np.fromfile(name1, dtype=np.uint8), -1)
                    img2 = cv2.imdecode(np.fromfile(name2, dtype=np.uint8), 0)
                    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
                    h, w = img2.shape
                    # All the 6 methods for comparison in a list
                    # methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                    # 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
                    
                    res = cv2.matchTemplate(img1, img2, cv2.TM_SQDIFF)
                    record.append(res[0, 0])
                    # if not os.path.exists(ssave_name):
                    #     os.makedirs(ssave_name)
                    # flag_ = 1
                    # shutil.copy(finasave_img, ssave_name)
                    break
            else:
                # general operation
                img1 = cv2.imdecode(np.fromfile(fimg_name, dtype=np.uint8), -1)
                img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
                res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
                record.append(res[0, 0])

            record = np.array(record)
            # record.shape[0] = 1
            print(record)
        exit(0)


if __name__ == '__main__':
    main('C')