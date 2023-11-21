import numpy as np
import os
import cv2 as cv

def fill_boundary(img1, img2):  # img均为灰度图
    height1, width1 = img1.shape
    height2, width2 = img2.shape
    height = max(height1, height2)
    width = max(width1, width2)
    img1 = cv.copyMakeBorder(img1, (height - height1) // 2, (height - height1) // 2,
                              (width - width1) // 2, (width - width1) // 2, cv.BORDER_CONSTANT)
    img2 = cv.copyMakeBorder(img2, (height - height2) // 2, (height - height2) // 2,
                              (width - width2) // 2, (width - width2) // 2, cv.BORDER_CONSTANT)
    img1 = cv.resize(img1, (width, height), interpolation=cv.INTER_CUBIC)
    img2 = cv.resize(img2, (width, height), interpolation=cv.INTER_CUBIC)
    return img1, img2

class BBox(object):

    def __init__(self, bbox):
        self.left = bbox[0]
        self.top = bbox[1]
        self.right = bbox[2]
        self.bottom = bbox[3]

def average_pic(path,out_path):  # path为读取img_mean.jpg的文件夹名称，如bin_resize，bin_rotation，bin_rotation2
    if not os.path.exists(out_path):#建立输出文件夹
        os.makedirs(out_path)
    name_list = os.listdir(path)

    #img_mean_mean = cv.cvtColor(img_mean_mean, cv.COLOR_RGB2GRAY)
    n = len(name_list)
    for name in name_list:
        img_black = np.zeros((1000, 1000, 3), np.uint8)
        img_black.fill(0)  # 创建黑色画布
        img_black = cv.cvtColor(img_black, cv.COLOR_RGB2GRAY)

        dir_input = os.path.join(path,name)
        pic_list = os.listdir(dir_input)
        print(pic_list)
        for m in pic_list:
            os.chdir(dir_input)
            img = cv.imread(m, cv.IMREAD_GRAYSCALE)
            #img = cv.imread(os.path.join(path, jujuba_name), cv.IMREAD_GRAYSCALE)
            img_black, img = fill_boundary(img_black, img)
            img_black = img_black + (img / n)

        _, img_black = cv.threshold(img_black, 127, 255, cv.THRESH_BINARY)
        img_black = cv.medianBlur(img_black.astype(np.uint8), 15)
        cv.imshow('img_black',img_black)
        cv.imwrite(os.path.join(out_path, f'{name}'), img_black)
    return img_black