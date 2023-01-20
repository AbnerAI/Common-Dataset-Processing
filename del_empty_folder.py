import os
# remove
path = '/media/oem/sda/cxx/DataForDivideTestForThesis/N'
list_ = os.listdir(path)
for itm in list_:
    new_f = os.path.join(path, itm)
    new_ff = os.listdir(new_f)
    if len(new_ff)==0:
        print(new_f)
        os.removedirs(new_f)
    else:
        del_flag = 0
        for ii in new_ff:
            if ii.endswith('.jpg'):
                del_flag = 1
                break
        if del_flag == 0:
            print(new_f)
            os.removedirs(new_f)
