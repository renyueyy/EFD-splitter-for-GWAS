import cv2 as cv
import numpy as np
import os

def black_division(input_path, output_path):
    """
        :param input_path: 输入文件的路径及名称
        :param output_path:输出文件的路径，不需要名称，是输出文件夹
        :return:
    """
    if not os.path.exists(output_path):#建立输出文件夹
        os.makedirs(output_path)
    name_list = os.listdir(input_path)#获得图片名称列表，作为循环列表

    for m in name_list:
        pic_path = os.path.join(input_path, m)
        image = cv.imread(pic_path)  # 读入图片

        pic_out_path = output_path+'/'+m+'/'#输出文件路径
        if not os.path.exists(pic_out_path):
            os.makedirs(pic_out_path)

        # 创建核结构
        kenel = np.ones((10, 10), np.uint8)
        img2 = cv.erode(image, kenel)

        b, g, r = cv.split(img2)  # 单通道处理

        # 二值化图片
        ret, image_blue = cv.threshold(b, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # OSTU阈值
        ret, image_green = cv.threshold(g, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # OSTU阈值
        ret, image_red = cv.threshold(r, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # OSTU阈值

        #ret, image_blue = cv.threshold(b, 50, 255, cv.THRESH_BINARY)
        blue_gauss = cv.GaussianBlur(image_blue, (5, 5), 0)
        #ret, image_green = cv.threshold(g, 50, 255, cv.THRESH_BINARY)
        green_gauss = cv.GaussianBlur(image_green, (5, 5), 0)
        #ret, image_red = cv.threshold(r, 50, 255, cv.THRESH_BINARY)
        red_gauss = cv.GaussianBlur(image_red, (5, 5), 0)

        add = cv.add(blue_gauss, red_gauss, green_gauss)

        # 轮廓提取
        contour = image.copy()
        (cnts, _) = cv.findContours(add, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 轮廓检测
        cv.drawContours(contour, cnts, -1, (0, 255, 0), 2)  # 绘制轮廓

        count = 0  # 图像个数
        margin = 20  # 裁剪边距
        draw_rect = image.copy()
        # 循环切割图片
        for i, contour in enumerate(cnts):
            area = cv.contourArea(contour)  # 计算包围形状的面积
            if area < 10000 or area > 200000:  # 过滤面积，选择>30000,<150000的对象
                continue
            count += 1
            x, y, w, h = cv.boundingRect(contour)  # 确定正外接矩形左下角坐标（x,y）、宽w和高h
            box = np.array([[x, y], [x + w, y],
                            [x + w, y + h], [x, y + h]])  # 确定正矩形四个角的坐标
            cv.drawContours(draw_rect, [box], 0, (0, 0, 255), 2)  # 绘制外接矩形
            h1, w1 = image.shape[:2]
            x1 = int(x + w / 2)
            y1 = int(y + h / 2)  # 获得图片中心点（x1，y1）
            rect = ((x1, y1), (w, h), 0)
            M2 = cv.getRotationMatrix2D((x1, y1), rect[2], 1)
            rotated_image = cv.warpAffine(image, M2, (w1 * 2, h1 * 2))
            rotated_canvas = rotated_image[y - margin:y + h + margin + 1, x - margin:x + w + margin + 1]
            cv.imwrite(pic_out_path + "{}.jpg".format(count), rotated_canvas)  # 保存切割图片

        # print("jujuba #{}".format(count))
        #cv.imwrite(pic_out_path + "rect.jpg", draw_rect)  # 绘制矩形在原图上

def blue_division(input_path, output_path):
    """
        :param input_path: 输入文件的路径及名称
        :param output_path:输出文件的路径，不需要名称，是输出文件夹
        :return:
    """
    if not os.path.exists(output_path):#建立输出文件夹
        os.makedirs(output_path)
    name_list = os.listdir(input_path)#获得图片名称列表，作为循环列表
    #print(name_list)

    for m in name_list:
        #print(m)
        pic_path = os.path.join(input_path, m)
        img = cv.imread(pic_path)# 读入图片
        height, width, deep = img.shape  # 对白色北京
        dst = np.zeros((height, width, 3), np.uint8)
        for i in range(height):  # 色彩反转
            for j in range(width):
                b, g, r = img[i, j]
                dst[i, j] = (255 - b, 255 - g, 255 - r)

        pic_out_path = output_path+'/'+m+'/'#输出文件路径
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
        cv.imshow('gaussedge', gaussedge)
        cv.imshow('blur', blur)


        count = 0  # 图像个数
        margin = 20  # 裁剪边距
        draw_rect = img.copy()
        # 循环切割图片
        for i, contour in enumerate(cnts):
            area = cv.contourArea(contour)  # 计算包围形状的面积
            if area < 10000 or area > 200000:  # 过滤面积，选择>30000,<150000的对象
                continue
            count += 1
            x, y, w, h = cv.boundingRect(contour)  # 确定正外接矩形左下角坐标（x,y）、宽w和高h
            box = np.array([[x, y], [x + w, y],
                            [x + w, y + h], [x, y + h]])  # 确定正矩形四个角的坐标
            cv.drawContours(draw_rect, [box], 0, (0, 0, 255), 2)  # 绘制外接矩形
            h1, w1 = img.shape[:2]
            x1 = int(x + w / 2)
            y1 = int(y + h / 2)  # 获得图片中心点（x1，y1）
            rect = ((x1, y1), (w, h), 0)
            M2 = cv.getRotationMatrix2D((x1, y1), rect[2], 1)
            rotated_image = cv.warpAffine(img, M2, (w1 * 2, h1 * 2))
            rotated_canvas = rotated_image[y - margin:y + h + margin + 1, x - margin:x + w + margin + 1]
            cv.imwrite(pic_out_path + "{}.jpg".format(count), rotated_canvas)  # 保存切割图片

        #print("jujuba #{}".format(count))
        #cv.imwrite(pic_out_path + "rect.jpg", draw_rect)  # 绘制矩形在原图上

def white_division(input,output):
    """
    :param input: 输入文件的路径及名称
    :param output:输出文件的路径，不需要名称，是输出文件夹
    :return:
    """
    img = cv.imread(input)#读入图片

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)#转换为hsv格式
    kenel = np.ones((10, 10), np.uint8)#卷积核
    kenel2 = np.ones((20, 20), np.uint8)#定义卷积核
    img2 = cv.GaussianBlur(hsv, (5, 5), 1)#高斯模糊
    b, g, r = cv.split(img2)#对高斯模糊后对图片进行单通道分离
    ret, image_green = cv.threshold(g, 65, 255, cv.THRESH_BINARY)#对单通道图片进行固定阈值二值化处理
    green_gauss = cv.GaussianBlur(image_green, (5, 5), 0)
    close_green = cv.morphologyEx(green_gauss, cv.MORPH_CLOSE, kenel2)

    height, width, deep = img.shape#对白色北京
    dst = np.zeros((height, width, 3), np.uint8)
    for i in range(height):  # 色彩反转
        for j in range(width):
            b, g, r = img[i, j]
            dst[i, j] = (255 - b, 255 - g, 255 - r)

    b, g, r = cv.split(dst)

    # 轮廓提取
    ret, image_g = cv.threshold(g, 170, 255, cv.THRESH_BINARY)
    g_gauss = cv.GaussianBlur(image_g, (5, 5), 0)
    close_g = cv.morphologyEx(g_gauss, cv.MORPH_CLOSE, kenel)

    add = cv.add(close_g, close_green)
    close_add = cv.morphologyEx(add, cv.MORPH_CLOSE, kenel2)
    contour = img.copy()

    (cnts, _) = cv.findContours(close_add, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 轮廓检测
    cv.drawContours(contour, cnts, -1, (0, 255, 0), 2)  # 绘制轮廓
    #gaussedge = cv.Canny(close_add, 0, 50)

    count = 0  # 图像个数
    margin = 10  # 裁剪边距
    draw_rect = img.copy()
    for i, contour in enumerate(cnts):
        area = cv.contourArea(contour)  # 计算包围形状的面积
        if area < 30000 or area > 380000:  # 过滤面积，选择>30000,<150000的对象
            continue
        count += 1
        x, y, w, h = cv.boundingRect(contour)  # 确定正外接矩形左下角坐标（x,y）、宽w和高h
        box = np.array([[x, y], [x + w, y],
                        [x + w, y + h], [x, y + h]])  # 确定正矩形四个角的坐标
        cv.drawContours(draw_rect, [box], 0, (255, 0, 0), 2)  # 绘制外接矩形
        h1, w1 = img.shape[:2]
        x1 = int(x + w / 2)
        y1 = int(y + h / 2)  # 获得图片中心点（x1，y1）
        rect = ((x1, y1), (w, h), 0)
        M2 = cv.getRotationMatrix2D((x1, y1), rect[2], 1)
        rotated_image = cv.warpAffine(img, M2, (w1 * 2, h1 * 2))
        rotated_canvas = rotated_image[y - margin:y + h + margin + 1, x - margin:x + w + margin + 1]
        cv.imwrite(output + "{}.jpg".format(count), rotated_canvas)  # 保存切割图片
    #cv.imwrite(output+"rect.jpg", draw_rect)
    return img



