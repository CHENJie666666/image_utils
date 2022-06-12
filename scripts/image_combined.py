"""
功能：拼接两张图片（左对齐、右对齐、上对齐、下对齐、垂直居中对齐、水平居中对齐）
"""

import numpy as np
from PIL import Image
import os
import argparse

def argv_parse():
    """
    创建命令行参数解析器
    """
    parser = argparse.ArgumentParser(description="拼接两张图片")

    parser.add_argument("-f", "--first_img_path", type=str, 
                            help="第一张图片路径")
    parser.add_argument("-s", "--second_img_path", type=str, 
                            help="第二张图片路径")
    parser.add_argument("-a", "--align", type=str, 
                            choices=['left', 'right', 'up', 'down', 'vcenter', 'hcenter'],
                            help="对齐方式：左对齐left、右对齐right、上对齐up、下对齐down、垂直居中对齐vcenter、水平居中对齐hcenter")                        
    parser.add_argument("-m", "--margin", default=0, type=int,
                            help="图片间距")
    parser.add_argument("-o", "--output", default='result.jpg', type=str,
                            help="输出图片路径")

    args = parser.parse_args()
    return args


def outer_combine_two_images(img1_path, img2_path, align, margin, save_file):
    """
    外拼接两张图片
    :params: img1_path str, 图片1路径
    :params: img1_path str, 图片2路径
    :params: align str, 对齐方式, left/right/up/down/vcenter/hcenter
    :params: margin int, 图片间隔
    """
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    
    # 对图片格式进行统一
    if (not img1_path.endswith('.png')) and img2_path.endswith('.png'):
        img1 = img1.convert('RGBA')
    elif img1_path.endswith('.png') and (not img2_path.endswith('.png')):
        img2 = img2.convert('RGBA')
    
    # 转化为ndarray格式
    img1 = np.array(img1, dtype=np.uint8)
    img2 = np.array(img2, dtype=np.uint8)

    h1, w1, c = img1.shape
    h2, w2, _ = img2.shape

    # 写入图片
    if align == 'left':
        # left_combine(img1, img2)
        dst = np.zeros((h1 + h2 + margin, max(w1, w2), c), np.uint8)
        startw = 0
        starth = h1 + margin

    elif align == 'right':
        dst = np.zeros((h1 + h2 + margin, max(w1, w2), c), np.uint8)
        startw = abs(w1 - w2)
        starth = h1 + margin

    elif align == 'vcenter':
        dst = np.zeros((h1 + h2 + margin, max(w1, w2), c), np.uint8)
        startw = int(abs(w1 - w2) / 2)
        starth = h1 + margin

    elif align == 'up':
        dst = np.zeros((max(h1, h2), w1 + w2 + margin, c), np.uint8)
        startw = w1 + margin
        starth = 0

    elif align == 'down':
        dst = np.zeros((max(h1, h2), w1 + w2 + margin, c), np.uint8)
        startw = w1 + margin
        starth = abs(h1 - h2)
    
    elif align == 'hcenter':
        dst = np.zeros((max(h1, h2), w1 + w2 + margin, c), np.uint8)
        startw = w1 + margin
        starth = int(abs(h1 - h2) / 2)

    dst = write_first_image(img1, dst)
    dst = write_second_image(img2, dst, starth, startw)

    # 保存合并图片
    if c == 3:
        save_file = save_file if not save_file.endswith('.png') \
            else os.path.splitext(save_file)[0] + '.jpg'
        Image.fromarray(dst).save(save_file, 'jpg')
        print(f'file has been save as {save_file}')
    else:
        save_file = save_file if save_file.endswith('.png') \
            else os.path.splitext(save_file)[0] + '.png'
        Image.fromarray(dst).save(save_file, 'png')
        print(f'file has been save as {save_file}')


def write_first_image(img, dst):
    for h in range(img.shape[0]):
        for w in range(img.shape[1]):
            if img.shape[2] == 3:
                (b, g, r) = img[h, w]
                dst[h, w] = (b, g, r)
            else:
                (b, g, r, a) = img[h, w]
                dst[h, w] = (b, g, r, a)
    return dst


def write_second_image(img, dst, starth, startw):
    for h in range(img.shape[0]):
        for w in range(img.shape[1]):
            if img.shape[2] == 3:
                (b, g, r) = img[h, w]
                dst[starth + h, startw + w] = (b, g, r)
            else:
                (b, g, r, a) = img[h, w]
                dst[starth + h, startw + w] = (b, g, r, a)
    return dst


if __name__ == '__main__':
    args = argv_parse()
    outer_combine_two_images(args.first_img_path, args.second_img_path, 
                        args.align, args.margin, args.output)

    # 运行示例
    # 拼接 1.png 和 2.png，对齐方式为左对齐，间隔 20 像素
    # python .\image_combined.py -f 1.png -s 2.png -a left -m 20 -o temp.png