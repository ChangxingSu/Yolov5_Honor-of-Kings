# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import argparse
 
parser = argparse.ArgumentParser()
#xml文件的地址，根据自己的数据进行修改 xml一般存放在Annotations下
parser.add_argument('--xml_path', default='Annotations',required=True, type=str, help='input xml label path')
#数据集的划分，地址选择自己数据下的ImageSets/Main
parser.add_argument('--txt_path', default='worktxt', type=str, help='output txt label path')
opt = parser.parse_args()

xmlfilepath = opt.xml_path
txtsavepath = opt.txt_path

sets = ['train', 'val', 'test']
classes = ["hero","grass","wild_monster","dragon","soldier","tower","buff","crystal"]   # 改成自己的类别
# abs_path = os.getcwd()
# print(abs_path)

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(image_id):
    in_file = open(xmlfilepath+'/%s.xml' % (image_id), encoding='UTF-8')
    out_file = open(txtsavepath+'/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
            float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

for image_set in sets:
    if not os.path.exists('worktxt/'):
        os.makedirs('worktxt/')
    image_ids = open('ImageSets/Main/%s.txt' % (image_set)).read().strip().split()
    list_file = open('%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write(abs_path + '/images/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()

