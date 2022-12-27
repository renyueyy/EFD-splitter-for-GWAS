import numpy as np
import cv2 as cv
import pyefd
import os

def efd_single(name,path,output):
    img_path = os.path.join(path,name)
    img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
    blurred = cv.GaussianBlur(img, (11, 11), 0)
    edge = cv.Canny(blurred, 5, 15)
    contours, _ = cv.findContours(edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    efds = pyefd.elliptic_fourier_descriptors(np.squeeze(contours))
    #print(efds)
    #txt_path = os.path.join('./rsz_images', name, 'efd.csv')
    txt_path = os.path.join(output,name)
    np.savetxt(txt_path+'.csv', efds, delimiter=',')

def efd_batch(path,output):
    if not os.path.exists(output):#建立输出文件夹
        os.makedirs(output)
    name_list = os.listdir(path)
    for name in name_list:
        efd_single(name,path,output)