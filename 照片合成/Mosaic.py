#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : AwesomeTang
# @File    : Resemble.py
# @Version : Python 3.7
# @Time    : 2019-06-23 13:52
import time

from PIL import Image
import os
import numpy as np


class Config:
    corp_size = 40
    filter_size = 50
    similarity = 10
    multiple = 6


def mapping_table(pic_folder='wechat'):
    """
    What this function do?
    1. transverse every image in PIC_FOLDER;
    2. resize every image in (8, 8) and covert into GREY;
    3. CODE for every image, CODE like [1, 0, 1, 1, 0....1]
    4. build a dict to gather all image and its CODE.
    :param pic_folder: path of pictures folder.
    :return: a dict
    """
    suffix = ['jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG']
    if not os.path.isdir(pic_folder):
        raise OSError('Folder [{}] is not exist, please check.'.format(pic_folder))

    pic_list = os.listdir(pic_folder)
    results = {}
    mean_dic = {}
    pic_dic = {}
    r_n = len(pic_list)
    for idx, pic in enumerate(pic_list):
        if pic.split('.')[-1] in suffix:
            path = os.path.join(pic_folder, pic)
            try:
                img = Image.open(path).resize((Config.corp_size, Config.corp_size), Image.ANTIALIAS).convert('RGB')
                img_gray = Image.open(path).resize((Config.corp_size, Config.corp_size), Image.ANTIALIAS).convert('L')
                for r in range(4):
                    if not r:
                        results[idx] = pic_code(np.array(img_gray.resize((8, 8), Image.ANTIALIAS)))
                        mean_dic[idx] = mean(img)
                        pic_dic[idx] = img
                    else:
                        img_r = img.rotate(90 * r)
                        img_gray_r = img_gray.rotate(90 * r)
                        results[idx + r * r_n] = pic_code(np.array(img_gray_r.resize((8, 8), Image.ANTIALIAS)))
                        mean_dic[idx + r * r_n] = mean(img_r)
                        pic_dic[idx + r * r_n] = img_r
            except OSError:
                pass
    return results, mean_dic, pic_dic
    # return pic_dic


def mean(image):
    if image.mode != "RGB":
        image = image.convert("RGB")
    pix = image.load()
    avg_r, avg_g, avg_b = 0, 0, 0
    n = 1
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b = pix[i, j]
            avg_r += r
            avg_g += g
            avg_b += b
            n += 1
    avg_r /= n
    avg_g /= n
    avg_b /= n
    return (avg_r, avg_g, avg_b)


def pic_code(image: np.ndarray):
    """
    To make a one-hot code for IMAGE.
    AVG is mean of the array(IMAGE).
    Traverse every pixel of IMAGE, if the pixel value is more then AVG, make it 1, else 0.
    :param image: an array of picture
    :return: A sparse list with length [picture's width * picture's height].
    """
    width, height = image.shape
    avg = image.mean()
    one_hot = np.array([1 if image[i, j] > avg else 0 for i in range(width) for j in range(height)])
    return one_hot


def img_filter(slice_mean, pictures_mean, filter_size):
    a = []
    similarity_list = []
    slice_r, slice_g, slice_b = slice_mean
    for key_, (v_r, v_g, v_b) in pictures_mean.items():
        cur_dif = abs(float(slice_r) - float(v_r)) + abs(float(slice_g) - float(v_g)) + abs(float(slice_b) - float(v_b))
        a.append((key_, cur_dif))
    # return sorted(a, key=lambda item: item[1])[:filter_size]
    s = sorted(a, key=lambda item: item[1])[:filter_size]
    for key_, dif_ in s:
        if dif_ - s[0][1] < Config.similarity:
            similarity_list.append(key_)
        else:
            break
    return similarity_list


class PicMosaicMerge:
    def __init__(self, pic_path, corp_size=20, pic_folder='wechat', multiple=1):
        """
        马赛克拼图
        :param pic_path: 马赛克拼图原图片路径
        :param corp_size: 子图片像素大小（长和宽）
        :param pic_folder: 子图片库目录路径
        :param multiple: 原图放大倍数
        """
        self.mapping_table, self.pictures_mean, self.pictures = mapping_table(pic_folder=pic_folder)
        # self.pictures = mapping_table(pic_folder=pic_folder)
        # self.picture = Image.open(pic_path).convert('L')
        self.picture = Image.open(pic_path).convert('RGB')
        self.corp_size = corp_size
        self.multiple = multiple

    def corp(self):
        flag = ['\\', '|', '/', '-']
        flag_num = 0
        width, height = self.picture.size
        width = (width // Config.corp_size) * Config.corp_size * self.multiple
        height = (height // Config.corp_size) * Config.corp_size * self.multiple
        self.picture = self.picture.resize((width, height), Image.ANTIALIAS)
        picture = np.array(self.picture)
        start_time = time.time()
        for i in range(height // Config.corp_size):
            for j in range(width // Config.corp_size):
                # slice_ = Image.fromarray(picture[i * Config.corp_size:(i + 1) * Config.corp_size, j * Config.corp_size:(j + 1) * Config.corp_size]).convert('RGB')
                slice_ = Image.fromarray(picture[i * Config.corp_size:(i + 1) * Config.corp_size, j * Config.corp_size:(j + 1) * Config.corp_size]).convert('L')
                slice_mean = mean(Image.fromarray(picture[i * Config.corp_size:(i + 1) * Config.corp_size, j * Config.corp_size:(j + 1) * Config.corp_size]))
                # slice_mean = picture[i * Config.corp_size:(i + 1) * Config.corp_size, j * Config.corp_size:(j + 1) * Config.corp_size].mean()
                candidate = img_filter(slice_mean, self.pictures_mean, Config.filter_size)
                # print(candidate)
                # candidate = sorted([(key_, abs(value_ - slice_mean)) for key_, value_ in self.pictures_mean.items()], key=lambda item: item[1])[:Config.filter_size]
                one_hot = pic_code(np.array(slice_.resize((8, 8), Image.ANTIALIAS)))
                a = [(key_, np.equal(one_hot, self.mapping_table[key_]).mean()) for key_ in candidate]
                a = max(a, key=lambda item: item[1])
                picture[i * Config.corp_size:(i + 1) * Config.corp_size, j * Config.corp_size:(j + 1) * Config.corp_size] = self.pictures[a[0]]
                print('\rSpent %ds..%s%.2f%% complete' % (time.time() - start_time, flag[flag_num % 4], (float(i) * float(width // Config.corp_size) + float(j + 1)) / float(width // Config.corp_size) / float(height // Config.corp_size) * 100.0), end='', flush=True)
                flag_num += 1
        picture = Image.fromarray(picture)
        picture.show()
        picture.save('result.jpg')


if __name__ == "__main__":
    p = PicMosaicMerge(pic_path='微信图片_20191018155449.jpg', pic_folder='origin_photos', multiple=Config.multiple)
    p.corp()