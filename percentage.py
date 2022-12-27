import numpy as np
import cv2 as cv
import pandas as pd
import pyefd
import os
from tqdm import tqdm

def overlape(path,output_path):
    name_list = os.listdir(path)
    all_over = []#创建重合率列表
    over = []
    for jujuba_name in tqdm(name_list):#遍历文件
        print(jujuba_name)
        image = cv.imread(path + jujuba_name,cv.IMREAD_GRAYSCALE)#读入原始轮廓图片
        contours, hierachy = cv.findContours(edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        original_area = cv.contourArea(contours[0])

        for i in range(1, 11):
            reconstrution_contours = get_reconstrution_contours(img, i)#获得重建图片（不保存
            img_allblack = np.zeros_like(img)
            reconstruction = cv2.drawContours(img_allblack, reconstrution_contours, -1, (255, 255, 255), -1)
            new = cv.addWeighted(image, 0.5, reconstruction, 0.5, 0)
            edge = cv.Canny(new, 100, 200)
            ret, new_pic = cv.threshold(edge, 127, 255, cv.THRESH_BINARY)

            cnts_new, hierachy = cv.findContours(new_pic, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            area = cv.contourArea(cnts_new)
            over_single = str(area / area_img)
            over.append(over_single)
            all_over.append(over)
        data = pd.DataFrame(all_over)
        data.to_csv(output_path + 'precentage.csv', sep=',', index=0, header=0)


        """
        img = cv.imread(path + jujuba_name, cv.IMREAD_GRAYSCALE)
        edge = cv.Canny(img, 100, 200)
        contours, hierachy = cv.findContours(edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        original_area = cv.contourArea(contours[0])
        over = [jujuba_name]
        area_img = 0  # 计算原图轮廓面积
        for n in contours:
            area_img += cv.contourArea(n)
        contours1, hierachy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        area_img1 = 0
        for n in contours1:
            area_img1 += cv.contourArea(n)
        tour1 = cv.drawContours(image, contours, -1, (0, 0, 255), 1)
        tour2 = cv.drawContours(tour1, contours1, -1, (255, 0, 0), 1)
        #cv.imshow("tour", tour2)

        for i in range(1, 11):
            reconstrution_path = os.path.join(path,name,i)
            reconstrution = cv.imread(reconstrution_path+'.jpg', cv.IMREAD_GRAYSCALE)
            # img1,reconstrution1 = fill_boundary(img, reconstrution)

            # new = (reconstrution + img) // 2
            new = cv.addWeighted(img, 0.5, reconstrution, 0.5, 0)
            ret, new_pic = cv.threshold(new, 130, 255, cv.THRESH_BINARY)

            cnts_new, hierachy = cv.findContours(new_pic, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            area = 0
            for m in cnts_new:
                area += cv.contourArea(m)
            # area = cv.contourArea(cnts_new[0])
            # reconstrution_area = cv2.contourArea(reconstrution_contours[0])
            # over_single = str(i)+"_"+str(area_new/area_img)
            over_single = str(area / area_img)
            over.append(over_single)
        print(over)
        all_over.append(over)
    data = pd.DataFrame(all_over)
    data.to_csv(output_path+'precentage.csv', sep=',', index=0, header=0)
        """