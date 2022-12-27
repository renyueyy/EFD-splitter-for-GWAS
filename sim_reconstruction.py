import cv2 as cv
import numpy as np
import os
import pyefd
from numpy import genfromtxt

def contour_reconstruction(coeffs):
    img = np.zeros((1000, 1000,3), np.uint8)
    img.fill(0)#创建黑色画布
    reconstrution = pyefd.reconstruct_contour(coeffs, locus=(500, 500), num_points=100000)
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
    #save_dirpath = os.path.join(output_path, name)
    #if not os.path.exists(save_dirpath):
    #    os.makedirs(save_dirpath)
    #cv.imwrite(os.path.join(save_dirpath, f'{i}.jpg'), img_allblack)
    #cv.imshow('img',resconstruction_pic)
    #cv.waitKey()

os.chdir('/Volumes/renyue-2T_A/my_project/simulation/1')#设置工作路径
my_data = genfromtxt("sim_traits.csv", delimiter=',')#把csv文件输入为numpy数组
save_path ="/Volumes/renyue-2T_A/my_project/simulation/1/pic/"
print(len(my_data))
for i in range(1,len(my_data)):
    print(i)
    coeffs = my_data[i,range(1,13)]
    coeffs = coeffs.reshape(3,4)
    black_background = contour_reconstruction(coeffs)
    cv.imshow('black',black_background)
    image = contour_reconstruction(coeffs)
    name = my_data[i,1]
    #cv.imshow('image',image)
    cv.imwrite(f'{save_path}{i}.jpg', black_background)
    #cv.waitKey()