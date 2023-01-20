# keep 1 file every folder
import os

def main():
    img_c = img_path + '/C/'
    img_n = img_path + '/N/'
    one_c_dir = os.listdir(img_c)
    one_n_dir = os.listdir(img_n)
    for itm in one_c_dir:
        f_path = img_c + itm
        f_ = os.listdir(f_path)
        c_len = len(f_)
        for idx, it in enumerate(f_):
            print(f_path + '/' + it)
            os.remove(f_path + '/' + it)
            if idx == c_len-2:
                break

    for itm in one_n_dir:
        f_path = img_n + itm
        f_ = os.listdir(f_path)
        n_len = len(f_)
        for idx, it in enumerate(f_):
            print(f_path + '/' + it)
            os.remove(f_path + '/' + it)
            if idx == n_len-2:
                break

if __name__ == '__main__':
    img_path = "/media/oem/sda21/cxx/breast_all/Video/All_Test_To_Pure_By_Nodules_Model_copy_del_repeat"
    main()