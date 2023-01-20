import os
# remove
path = '/media/oem/sda/cxx/DataForDivideTestForThesis'
for parent,dirnames,filenames in os.walk(os.path.dirname(path)):
    filenames[:] = [f for f in filenames if f.endswith("error")]
    for filename in filenames:
        #输出找到的文件目录
        os.remove(os.path.join(parent,filename))