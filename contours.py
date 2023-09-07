import cv2 as cv
import numpy as np
import os

def black_background(input_path,output_path):
    """
    #黑色背景下图片轮廓的提取
    :param input_division: 分割后图片的文件夹（只写到文件夹，每个文件夹内的图片在函数里循环读入）
    :param output_gaussedge: 提取轮廓后图片的保存路径
    :return:
    """
    if not os.path.exists(output_path):#建立输出文件夹
        os.makedirs(output_path)
    dir_list = os.listdir(input_path)#获得图片名称列表，作为循环列表
    average_area = []
    for dir in dir_list:
        dir_input = input_path+'/'+dir
        pic_list = os.listdir(dir_input)
        dir_output = output_path+'/'+dir
        if not os.path.exists(dir_output):  # 建立输出文件夹
            os.makedirs(dir_output)

        count = 0
        for m in pic_list:
            count +=1
            img = cv.imread(dir_input+'/'+m)  # 读入图片

            # 原图片腐蚀处理
            # 创建核结构
            kenel = np.ones((5, 5), np.uint8)
            img2 = cv.GaussianBlur(img, (5, 5), 1)

            # 单通道处理
            b, g, r = cv.split(img2)

            # 图片二值化，分别提取rgb三通道图片
            #ret, image_blue = cv.threshold(b, 75, 255, cv.THRESH_BINARY)
            ret, image_blue = cv.threshold(b, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # OSTU阈值
            blue_gauss = cv.GaussianBlur(image_blue, (5, 5), 0)
            close_blue = cv.morphologyEx(blue_gauss, cv.MORPH_CLOSE, kenel)

            #ret, image_green = cv.threshold(g, 75, 255, cv.THRESH_BINARY)
            ret, image_green = cv.threshold(g, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # OSTU阈值
            green_gauss = cv.GaussianBlur(image_green, (5, 5), 0)
            close_green = cv.morphologyEx(green_gauss, cv.MORPH_CLOSE, kenel)

            #ret, image_red = cv.threshold(r, 75, 255, cv.THRESH_BINARY)
            ret, image_red = cv.threshold(r, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # OSTU阈值
            red_gauss = cv.GaussianBlur(image_red, (5, 5), 0)
            close_red = cv.morphologyEx(red_gauss, cv.MORPH_CLOSE, kenel)

            add = cv.add(close_red, close_blue, close_green)  # 二值化图片叠加
            add2 = cv.erode(add, kenel)  # 闭运算

            # 提取轮廓
            contour = add2.copy()
            (cnts, add_image) = cv.findContours(add, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 轮廓检测
            gaussedge = cv.drawContours(contour, cnts, -1, (0, 255, 0), 2)  # 绘制轮廓
            blur = cv.medianBlur(gaussedge, 21)  # 中值滤波平滑边缘
            cv.imwrite(dir_output + f"/{count}.jpg", blur)

            # 计算轮廓面积
            areas = []
            area = 0
            for n in cnts:
                area += cv.contourArea(n)
            areas = np.append(areas, area)
        average = np.mean(areas)
        print(dir,':',average)
        average_area = np.append(average_area,average)
    average_all = np.mean(average_area)
    print('all_average',average_all)
    return


def other_background(input_path,output_path):
    """
    #黑色背景下图片轮廓的提取
    :param input_division: 分割后图片的文件夹（只写到文件夹，每个文件夹内的图片在函数里循环读入）
    :param output_gaussedge: 提取轮廓后图片的保存路径
    :return:
    """
    if not os.path.exists(output_path):#建立输出文件夹
        os.makedirs(output_path)
    dir_list = os.listdir(input_path)#获得图片名称列表，作为循环列表
    average_area = []
    for dir in dir_list:
        dir_input = input_path+'/'+dir
        pic_list = os.listdir(dir_input)
        dir_output = output_path+'/'+dir
        if not os.path.exists(dir_output):  # 建立输出文件夹
            os.makedirs(dir_output)

        count = 0
        for m in pic_list:
            count +=1
            img = cv.imread(dir_input+'/'+m)  # 读入图片

            # 原图片腐蚀处理
            # 创建核结构
            height, width, deep = img.shape  # 对白色北京
            dst = np.zeros((height, width, 3), np.uint8)
            for i in range(height):  # 色彩反转
                for j in range(width):
                    b, g, r = img[i, j]
                    dst[i, j] = (255 - b, 255 - g, 255 - r)

            pic_out_path = output_path + '/' + m + '/'  # 输出文件路径
            if not os.path.exists(pic_out_path):
                os.makedirs(pic_out_path)

            hsv = cv.cvtColor(dst, cv.COLOR_BGR2HSV)  # 转换为hsv格式

            kenel = np.ones((10, 10), np.uint8)  # 卷积核
            img2 = cv.GaussianBlur(hsv, (5, 5), 1)  # 高斯模糊
            cv.imshow('hsv', img2)
            b, g, r = cv.split(img2)  # 对高斯模糊后对图片进行单通道分离

            # ret, image_green = cv.threshold(g, 65, 255, cv.THRESH_BINARY)  # 对单通道图片进行固定阈值二值化处理
            ret, image_blue = cv.threshold(b, 10, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
            blue_gauss = cv.GaussianBlur(image_blue, (5, 5), 0)
            close_blue = cv.morphologyEx(blue_gauss, cv.MORPH_CLOSE, kenel)

            contour = img.copy()
            blur = cv.medianBlur(close_blue, 5)  # 中值滤波平滑边缘

            # blur_1 = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
            (cnts, _) = cv.findContours(blur, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 轮廓检测
            gaussedge = cv.drawContours(contour, cnts, -1, (0, 0, 255), 2)  # 绘制轮廓
            blur = cv.medianBlur(gaussedge, 21)  # 中值滤波平滑边缘
            cv.imwrite(dir_output + f"/{count}.jpg", blur)

            # 计算轮廓面积
            areas = []
            area = 0
            for n in cnts:
                area += cv.contourArea(n)
            areas = np.append(areas, area)
        average = np.mean(areas)
        print(dir,':',average)
        average_area = np.append(average_area,average)
    average_all = np.mean(average_area)
    print('all_average',average_all)
    return


def white_background(input_path,output_path):
    """
    #黑色背景下图片轮廓的提取
    :param input_division: 分割后图片的文件夹（只写到文件夹，每个文件夹内的图片在函数里循环读入）
    :param output_gaussedge: 提取轮廓后图片的保存路径
    :return:
    """
    if not os.path.exists(output_path):#建立输出文件夹
        os.makedirs(output_path)
    dir_list = os.listdir(input_path)#获得图片名称列表，作为循环列表
    average_area = []
    for dir in dir_list:
        dir_input = input_path+'/'+dir
        pic_list = os.listdir(dir_input)
        dir_output = output_path+'/'+dir
        if not os.path.exists(dir_output):  # 建立输出文件夹
            os.makedirs(dir_output)

        count = 0
        for m in pic_list:
            count +=1
            img = cv.imread(dir_input+'/'+m)  # 读入图片

            # 原图片腐蚀处理
            # 创建核结构
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)  # 转换为hsv格式
            kenel = np.ones((10, 10), np.uint8)  # 卷积核
            kenel2 = np.ones((20, 20), np.uint8)
            img2 = cv.GaussianBlur(hsv, (5, 5), 1)  # 高斯模糊
            b, g, r = cv.split(img2)  # 单通道处理
            # ret,image_green = cv.threshold(g, 65, 255, cv.THRESH_BINARY)#固定阈值二值化
            ret, image_green = cv.threshold(g, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
            green_gauss = cv.GaussianBlur(image_green, (5, 5), 0)  # 高斯模糊
            close_green = cv.morphologyEx(green_gauss, cv.MORPH_CLOSE, kenel2)  # 闭运算

            height, width, deep = img.shape
            dst = np.zeros((height, width, 3), np.uint8)
            for i in range(height):  # 色彩反转
                for j in range(width):
                    b, g, r = img[i, j]
                    dst[i, j] = (255 - b, 255 - g, 255 - r)

            b, g, r = cv.split(dst)

            # 二值化处理
            # ret,image_g = cv.threshold(g,170, 255, cv.THRESH_BINARY)
            ret, image_g = cv.threshold(g, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # OSTU阈值
            g_gauss = cv.GaussianBlur(image_g, (5, 5), 0)  # 高斯模糊

            add = cv.add(g_gauss, close_green)  # hsv和
            # add = cv.add(blue_gauss,green_gauss)
            close_add = cv.morphologyEx(add, cv.MORPH_CLOSE, kenel2)

            # 提取轮廓
            contour = add.copy()
            (cnts, add_image) = cv.findContours(add, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 轮廓检测
            gaussedge = cv.drawContours(contour, cnts, -1, (0, 255, 0), 2)  # 绘制轮廓
            blur = cv.medianBlur(gaussedge, 21)  # 中值滤波平滑边缘
            cv.imwrite(dir_output + f"/{count}.jpg", blur)

            # 计算轮廓面积
            areas = []
            area = 0
            for n in cnts:
                area += cv.contourArea(n)
            areas = np.append(areas, area)
        average = np.mean(areas)
        print(dir,':',average)
        average_area = np.append(average_area,average)
    average_all = np.mean(average_area)
    print('all_average',average_all)
    return
