import numpy as np
import cv2 as cv
import pyefd
import os
from tqdm import tqdm
import pandas as pd


def get_single_parameters(name, n, input):  # name为品种图片名字，如1-1(L1-1).jpg，n为要获取的参数为1-20
    #coeffs_path = os.path.join('./rsz_images', name, 'efd.csv')
    coeffs_path = input + f'/edf/{name}'#输入文件所在文件夹
    coeffs = np.loadtxt(coeffs_path, delimiter=',')
    coeffs = coeffs.reshape((-1))
    return coeffs[n - 1]


def get_reconstrution_contours(name, n,input):
    contour =  np.zeros((1000, 1000, 3), np.uint8)
    coeffs = get_single_parameters(name, n, input)
    locus = pyefd.calculate_dc_coefficients(contour)
    reconstrution = pyefd.reconstruct_contour(coeffs, locus, contour.shape[0])
    reconstrution = np.rint(reconstrution).astype(np.int_)
    reconstrution_contours = [reconstrution.reshape(reconstrution.shape[0], -1, reconstrution.shape[1])]
    return reconstrution_contours


def contour_reconstruction_single_imgsave(name,inputpath,output_path,):  # name为品种图片名字，如1-1(L1-1).jpg
    img = cv.imread(os.path.join(inputpath,name))
    for i in range(1, 11):
        reconstrution_contours = get_reconstrution_contours(img, i,output_path)
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
