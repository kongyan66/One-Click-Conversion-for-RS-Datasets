import os 
import glob
import random
import shutil
import os.path as osp
from shutil import copyfile

from tqdm import tqdm

random.seed(666)

def copyfiles(src_files, dst_folder, is_plane = False):
    pbar = tqdm(src_files)
    for file in pbar:
        pbar.set_description("Creating {}:".format(dst_folder))
        if not is_plane:
            filename = os.path.split(file)[1]
        else: 
            _filename = os.path.split(file)[1]
            name, ext = os.path.splitext(_filename)
            filename = 'P' + str(int(name.strip('P')) + 510).zfill(4) + ext
        dstfile = os.path.join(dst_folder, filename)
        # print(dstfile)
        shutil.copyfile(file, dstfile)


def rewrite_label(annos, dst_folder, is_plane = False):
    pbar = tqdm(annos)
    for file in pbar:
        pbar.set_description("Rewriting to {}:".format(dst_folder))
        if not is_plane:
            filename = os.path.split(file)[1]
        else: 
            _filename = os.path.split(file)[1]
            name, ext = os.path.splitext(_filename)
            filename = 'P' + str(int(name.strip('P')) + 510).zfill(4) + ext
        dstfile = os.path.join(dst_folder, filename)
        # print(dstfile)
        with open(dstfile, 'w') as fw:
            with open(file, 'r') as f:
                _lines = f.readlines()
                if is_plane:
                    lines = ['airplane  ' + x for x in _lines]  
                else:
                    lines = ['car  ' + x for x in _lines]  
                content = ''.join(lines)
                fw.write(content)
# 将car和plane路径下图片和标签汇总汇总到一起（同时做了标签的预处理）
def creat_tree(root_dir):
    if not os.path.exists(root_dir):
        raise RuntimeError('invalid dataset path!')
    os.mkdir(os.path.join(root_dir, 'AllImages'))
    os.mkdir(os.path.join(root_dir, 'Annotations'))
    car_imgs = glob.glob(os.path.join(root_dir, 'CAR/*.png'))
    car_annos = glob.glob(os.path.join(root_dir, 'CAR/P*.txt'))
    airplane_imgs = glob.glob(os.path.join(root_dir, 'PLANE/*.png'))
    airplane_annos = glob.glob(os.path.join(root_dir, 'PLANE/P*.txt'))   
    copyfiles(car_imgs,  os.path.join(root_dir, 'AllImages') ) 
    copyfiles(airplane_imgs,  os.path.join(root_dir, 'AllImages'), True)
    rewrite_label(car_annos, os.path.join(root_dir, 'Annotations'))
    rewrite_label(airplane_annos, os.path.join(root_dir, 'Annotations'), True)

# 根据ImageSets划分数据集：train，val, test
def dataset_partition(data_dir):
    train_dir = osp.join(data_dir,'Train')
    val_dir = osp.join(data_dir,'Val')
    test_dir = osp.join(data_dir, 'Test')
    imgsets = osp.join(data_dir, 'ImageSets')
    trainset = osp.join(imgsets, 'train.txt')
    valset = osp.join(imgsets, 'val.txt')
    testset = osp.join(imgsets, 'test.txt')

    train_dirs = [train_dir, val_dir, test_dir]
    trainsets = [trainset, valset, testset]
    datatypes = ['train', 'val', 'test']
    for idx, train_dir in enumerate(train_dirs):
        datatype = datatypes[idx]
        trainset = trainsets[idx]
        if os.path.exists(train_dir):
            shutil.rmtree(train_dir)
        os.makedirs(osp.join(train_dir, 'images'))
        os.makedirs(osp.join(train_dir, 'annotations'))
        with open(trainset, 'r') as f1:
            train_content = f1.readlines()
        trainbar = tqdm(train_content)
        for trf in trainbar:
            trainbar.set_description(datatype + " partition")
            src_im = osp.join(data_dir + '/AllImages', trf.strip() + '.png')
            dst_im = osp.join(train_dir + '/images', trf.strip() + '.png')
            src_an = osp.join(data_dir + '/Annotations', trf.strip() + '.txt')
            dst_an = osp.join(train_dir + '/annotations', trf.strip() + '.txt')
            copyfile(src_im, dst_im)
            copyfile(src_an, dst_an)

# 转化数据集为DOTA格式（单独生成DOTA格式的TXT标注）
def generate_txt_labels(root_path):
    img_path = osp.join(root_path, 'images')
    label_path = osp.join(root_path, 'annotations')
    label_txt_path = osp.join(root_path, 'labelTxt')
    if  osp.exists(label_txt_path):
        shutil.rmtree(label_txt_path)
    os.mkdir(label_txt_path)

    img_names = [osp.splitext(img_name.strip())[0] for img_name in os.listdir(img_path)]
    pbar = tqdm(img_names)
    for img_name in pbar:
        pbar.set_description("UCAS-AOD generate_txt in {}".format(root_path))
        label = osp.join(label_path, img_name+'.txt')
        label_txt = osp.join(label_txt_path, img_name+'.txt')
        f_label = open(label)
        lines = f_label.readlines()
        s = ''
        for line in lines:
            classname, *box, cx, cy, w, h, t = line.strip().split()
            s += ' '.join(box) + ' ' + classname + ' 0\n' 
        f_label.close()
        with open(label_txt, 'w') as fw_label:
            fw_label.write(s)

if __name__ == "__main__":
    root_dir = 'data/UCAS_AOD'
    # 数据集准备阶段
    creat_tree(root_dir) 
    dataset_partition(root_dir)
    # 数据集转换阶段
    generate_txt_labels('data/UCAS_AOD/Train')
    generate_txt_labels('data/UCAS_AOD/Val')
    generate_txt_labels('data/UCAS_AOD/Test')
    print('converter done!')
