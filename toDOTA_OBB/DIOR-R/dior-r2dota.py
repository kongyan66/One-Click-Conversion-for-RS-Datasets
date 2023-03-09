import os
import os.path as osp

import xmltodict
import shutil
from tqdm import tqdm
from shutil import copyfile

# TODO
# 根据ImageSets划分图片和标注为三部分：train，val, test
def dataset_partition(data_dir):
    train_dir = osp.join(data_dir,'Train')
    val_dir = osp.join(data_dir,'Val')
    # trainval_dir = osp.join(data_dir,'Trainval')
    test_dir = osp.join(data_dir, 'Test')
    imgsets = osp.join(data_dir, 'ImageSets')
    trainset = osp.join(imgsets, 'Main', 'train.txt')
    valset = osp.join(imgsets, 'Main', 'val.txt')
    # trainvelset = osp.join(imgsets, 'trainval.txt')
    testset = osp.join(imgsets, 'Main', 'test.txt')

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
        if train_dir != test_dir:
            with open(trainset, 'r') as f1:
                train_content = f1.readlines()
            trainbar = tqdm(train_content)
            for trf in trainbar:
                trainbar.set_description(datatype + " partition")
                src_im = osp.join(data_dir + '/JPEGImages-trainval', trf.strip() + '.jpg')
                dst_im = osp.join(train_dir + '/images', trf.strip() + '.jpg')
                src_an = osp.join(data_dir + '/Annotations/Oriented Bounding Boxes', trf.strip() + '.xml')
                dst_an = osp.join(train_dir + '/annotations', trf.strip() + '.xml')
                copyfile(src_im, dst_im)
                copyfile(src_an, dst_an)
        # 测试集图片单独在一个文件夹内故单独处理
        else:
            with open(trainset, 'r') as f1:
                train_content = f1.readlines()
            trainbar = tqdm(train_content)
            for trf in trainbar:
                trainbar.set_description(datatype + " partition")
                src_im = osp.join(data_dir + '/JPEGImages-test', trf.strip() + '.jpg')
                dst_im = osp.join(train_dir + '/images', trf.strip() + '.jpg')
                src_an = osp.join(data_dir + '/Annotations/Oriented Bounding Boxes', trf.strip() + '.xml')
                dst_an = osp.join(train_dir + '/annotations', trf.strip() + '.xml')
                copyfile(src_im, dst_im)
                copyfile(src_an, dst_an)

# 转换为DOTA标注格式
def generate_txt_labels(root_path):
    img_path = osp.join(root_path, 'images')
    label_path = osp.join(root_path, 'annotations')
    label_txt_path = osp.join(root_path, 'labelTxt')
    if not osp.exists(label_txt_path):
        os.mkdir(label_txt_path)

    img_names = [osp.splitext(img_name.strip())[0] for img_name in os.listdir(img_path)]
    pbar = tqdm(img_names)
    for img_name in pbar:
        pbar.set_description("DIOR-R Preparation...")

        label = osp.join(label_path, img_name+'.xml')
        label_txt = osp.join(label_txt_path, img_name+'.txt')
        f_label = open(label)
        data_dict = xmltodict.parse(f_label.read())
        data_dict = data_dict['annotation']
        f_label.close()
        label_txt_str = ''
        # with annotations
        if data_dict['object']:
            objects = data_dict['object']
            bboxes, labels, bboxes_ignore, labels_ignore = parse_ann_info(
                objects)
            ann = dict(
                bboxes=bboxes,
                labels=labels,
                bboxes_ignore=bboxes_ignore,
                labels_ignore=labels_ignore)
            label_txt_str = ann_to_txt(ann)
        with open(label_txt,'w') as f_txt:
            f_txt.write(label_txt_str)

# 处理每个xml的标签
def parse_ann_info(objects):
    bboxes, labels, bboxes_ignore, labels_ignore = [], [], [], []
    # only one annotation
    if type(objects) != list:
        objects = [objects]
    for obj in objects:
        
        label = obj['name']
        obj_box = obj['robndbox']
        bbox = [float(obj_box['x_left_top']), float(obj_box['y_left_top']), 
               float(obj_box['x_right_top']), float(obj_box['y_right_top']), 
               float(obj_box['x_right_bottom']),  float(obj_box['y_right_bottom']),
               float(obj_box['x_left_bottom']),  float(obj_box['y_left_bottom'])]
        bboxes.append(bbox)
        labels.append(label)
  
    return bboxes, labels, bboxes_ignore, labels_ignore
# 生成TXT文件
def ann_to_txt(ann):
    out_str = ''
    for bbox, label in zip(ann['bboxes'], ann['labels']):
        str_line = '{} {} {} {} {} {} {} {} {} {}\n'.format(
            bbox[0], bbox[1], bbox[2], bbox[3], bbox[4], bbox[5], bbox[6], bbox[7], label, '0')
        out_str += str_line
    for bbox, label in zip(ann['bboxes_ignore'], ann['labels_ignore']):
        str_line = '{} {} {} {} {} {} {} {} {} {}\n'.format(
            bbox[0], bbox[1], bbox[2], bbox[3], bbox[4], bbox[5], bbox[6], bbox[7], label, '1')
        out_str += str_line
    return out_str



if __name__ == '__main__':
    # 存放DIOR-R数据集的路径
    dior_r_dir = '/home/z/code/kch/RS_Dataset/DIOR-R'
    # 数据准备阶段
    #dataset_partition(dior_r_dir)
    # 格式转换阶段
    generate_txt_labels(dior_r_dir + '/Train')
    generate_txt_labels(dior_r_dir + '/Val')
    generate_txt_labels(dior_r_dir + '/Test')

    print('converter done!')