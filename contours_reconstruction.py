import numpy as np
import cv2 as cv
import pyefd
import os
from tqdm import tqdm
import pandas as pd


def get_reconstrution_contours(img, n):
    edge = cv.Canny(img, 100, 200)
    contours, hierachy = cv.findContours(edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    contour = np.squeeze(contours)
    coeffs = pyefd.elliptic_fourier_descriptors(contour)
    coeffs = coeffs[0:n]
    locus = pyefd.calculate_dc_coefficients(contour)
    reconstrution = pyefd.reconstruct_contour(coeffs, locus, contour.shape[0])
    reconstrution = np.rint(reconstrution).astype(np.int_)
    reconstrution_contours = [reconstrution.reshape(reconstrution.shape[0], -1, reconstrution.shape[1])]
    return reconstrution_contours

def reconstrution_area_ratio(img,n):  # img需要提取轮廓的图片，10个参数的重建轮廓与圆面积比值(百分数)
    reconstrution_contours = get_reconstrution_contours(img, n)
    edge = cv.Canny(img, 100, 200)
    contours, hierachy = cv.findContours(edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    original_area = cv.contourArea(contours[0])
    reconstrution_area = cv.contourArea(reconstrution_contours[0])
    reconstrution_area_ratio = reconstrution_area / original_area * 100
    return reconstrution_area_ratio

def contour_reconstruction_single_imgsave(name,inputpath,output_path):  # name为品种图片名字，如1-1(L1-1).jpg
    img = cv.imread(os.path.join(inputpath,name))
    for i in range(1, 11):
        reconstrution_contours = get_reconstrution_contours(img, i)
        img_allblack = np.zeros_like(img)
        cv.drawContours(img_allblack, reconstrution_contours, -1, (255, 255, 255), -1)
        save_dirpath = os.path.join(output_path, name)
        if not os.path.exists(save_dirpath):
            os.makedirs(save_dirpath)
        cv.imwrite(os.path.join(save_dirpath, f'{i}.jpg'), img_allblack)

def contour_reconstruction_batch_imgsave(input_path,output_path):
    name_list = os.listdir(input_path)
    if not os.path.exists(output_path):#建立输出文件夹
        os.makedirs(output_path)
    for jujuba_name in tqdm(name_list):
        contour_reconstruction_single_imgsave(jujuba_name,input_path,output_path)

def overlape(path, output_path):
    name_list = os.listdir(path)
    all_over = []  # 创建重合率列表

    for name in tqdm(name_list):  # 遍历文件
        over = []
        over.append(name)
        image = cv.imread(os.path.join(path,name), cv.IMREAD_GRAYSCALE)  # 读入原始轮廓图片
        #ret, im = cv.threshold(image, 130, 255, cv.THRESH_BINARY)
        edge_image = cv.Canny(image, 0, 250)
        image1 = cv.imread(os.path.join(path, name))
        contours, hierachy = cv.findContours(edge_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        original_area = 0
        for n in contours:#求原始轮廓面积
            original_area += cv.contourArea(n)

        for i in range(1, 11):#i级傅立叶系数重建，求重合率，循环
            reconstrution_contours = get_reconstrution_contours(image, i)  # 获得重建图片（不保存
            img_allblack = np.zeros_like(image)
            reconstruction = cv.drawContours(img_allblack, reconstrution_contours, -1, (255, 255, 255), -1)
            new1 = cv.addWeighted(image, 0.5, reconstruction, 0.5, 0)#原图和重建轮廓叠加
            new = (image/2) + (reconstruction/2)
            cv.imshow('new', new)
            cv.imshow('new1',new1)
            cv.imshow('re', reconstruction)

            ret, new_pic = cv.threshold(new1, 200, 255, cv.THRESH_BINARY)
            edge = cv.Canny(new_pic, 200, 255)  # 找出重合轮廓
            #cv.imshow('edge', edge)
            cv.imshow('new_pic', new_pic)
            #cv.waitKey()

            cnts_new, hierachy = cv.findContours(edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            #cnts_new, hierachy = cv.findContours(new_pic, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            #a = cv.drawContours(image1, cnts_new, -1, (0, 0, 255), 1)
            b = cv.drawContours(image1, cnts_new, -1, (0, 0, 255), 1)
            #cv.imshow('canny', a)
            cv.imshow('cnts', b)
            #cv.waitKey()
            area = cv.contourArea(cnts_new[0])#计算重合面积
            over_single = str(area / original_area)
            over.append(over_single)
        all_over.append(over)
        data = pd.DataFrame(all_over)
        data.to_csv(output_path + 'precentage.csv', sep=',', index=0, header=0)



def percent(input_path,output_path):
    name_list = os.listdir(input_path)
    all_over = []  # 创建重合率列表

    for name in tqdm(name_list):  # 遍历文件
        over = []#创建储存重合率的列表
        over.append(name)
        image = cv.imread(os.path.join(input_path, name), cv.IMREAD_GRAYSCALE)  # 读入原始轮廓图片
        for i in range(1,11):
            percent = reconstrution_area_ratio(image, i)
            over.append(percent)
        all_over.append(over)
    data = pd.DataFrame(all_over)
    data.to_csv(output_path + 'precentage.csv', sep=',', index=0, header=0)