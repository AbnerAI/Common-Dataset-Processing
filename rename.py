import os

root = '/home/qianxianserver/data/cxx/breast_all/breast/视频-2021-2/2021_breast_three_classification_zk2/Pure/New/'
test_c_path = root + 'Test/C/'
test_n_path = root + 'Test/N/'
train_c_path = root + 'Train/C/'
train_n_path = root + 'Train/N/'

test_c_lists = os.listdir(test_c_path)
test_n_lists = os.listdir(test_n_path)
train_c_lists = os.listdir(train_c_path)
train_n_lists = os.listdir(train_n_path)

for itm in test_c_lists:
    os.rename(test_c_path + itm, test_c_path + itm + '_c')

for itm in test_n_lists:
    os.rename(test_n_path + itm, test_n_path + itm + '_n')

for itm in train_c_lists:
    os.rename(train_c_path + itm, train_c_path + itm + '_c')

for itm in train_n_lists:
    os.rename(train_n_path + itm, train_n_path + itm + '_n')