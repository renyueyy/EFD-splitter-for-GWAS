import cv2 as cv
import numpy as np
import os
import pyefd
from numpy import genfromtxt

def contour_reconstruction(coeffs):
    img = np.zeros((600, 600,3), np.uint8)
    img.fill(0)#创建黑色画布
    reconstrution = pyefd.reconstruct_contour(coeffs, locus=(300, 300), num_points=100000)
    reconstrution = np.rint(reconstrution).astype(np.int_)
    reconstrution_contours = [reconstrution.reshape(reconstrution.shape[0], -1, reconstrution.shape[1])]
    cv.drawContours(img, reconstrution_contours, -1, (255, 255, 255), -1)
    return img

def draw_contours_00(image,img):
    img0 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    (cnts,_ ) = cv.findContours(img0, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 轮廓检测
    resconstruction_pic = cv.drawContours(image, cnts, -1, (255, 0, 0), 2)  # 绘制轮廓
    return resconstruction_pic

def draw_contours_01(image,img):
    img0 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    (cnts, _) = cv.findContours(img0, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 轮廓检测
    resconstruction_pic = cv.drawContours(image, cnts, -1, (0,255, 0), 2)  # 绘制轮廓
    return resconstruction_pic

def draw_contours_11(image,img):
    img0 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    (cnts, _) = cv.findContours(img0, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 轮廓检测
    resconstruction_pic = cv.drawContours(image, cnts, -1, (0, 0, 255), 2)  # 绘制轮廓
    return resconstruction_pic

def save(data_path,save_path):
    """
    my_data:the pathway of input table
    :return:
    """
    my_data = genfromtxt(data_path, delimiter=',')  # 把csv文件输入为numpy数组
    n = 1
    for i in range(1, len(my_data)):
        coeffs = my_data[i, range(4, 16)]
        coeffs = coeffs.reshape(3, 4)
        black_background = contour_reconstruction(coeffs)
        cv.imshow('black', black_background)
        # cv.waitKey()

        if n == 3:
            image11 = draw_contours_11(image01, black_background)
            cv.imshow('image11', image11)
            n = 1
            chr = my_data[i - 2, 0]
            bp = my_data[i - 2, 1]
            cv.imwrite(f'{save_path}chr{chr}_{bp}.jpg', image11)

        else:
            if n == 2:
                image01 = draw_contours_01(image00, black_background)
                cv.imshow('image01', image01)
                n += 1
            if n == 1:
                image = np.zeros((600, 600, 3), np.uint8)
                image.fill(255)  # 创建白色画布
                image00 = draw_contours_00(image, black_background)
                cv.imshow('image00', image00)
                n += 1