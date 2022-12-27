import os
import cv2 as cv
import numpy as np

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

def rotation(m, img):  # m为旋转角度，img为灰度图
    '''
    将图片旋转m角度
    :param m:旋转角度
    :param img: 要旋转的图片，灰度图
    :return: 旋转后的图片
    '''
    height, width = img.shape
    center = (height / 2, width / 2)
    rot_mat = cv.getRotationMatrix2D(center, m, 1)
    img_rot = cv.warpAffine(img, rot_mat, (img.shape[1], img.shape[0]))
    return img_rot

def average_pic(path):  # path为读取img_mean.jpg的文件夹名称，如bin_resize，bin_rotation，bin_rotation2
    jujuba_name_list = os.listdir(path)
    img0 = cv.imread(os.path.join(path,jujuba_name_list[0]),cv.IMREAD_GRAYSCALE)
    img_black = np.zeros_like(img0)
    #img_mean_mean = cv.cvtColor(img_mean_mean, cv.COLOR_RGB2GRAY)
    n = len(jujuba_name_list)
    for jujuba_name in jujuba_name_list:
        img = cv.imread(os.path.join(path,jujuba_name), cv.IMREAD_GRAYSCALE)
        img_black, img = fill_boundary(img_black, img)
        img_black = img_black + (img / n)
    _, img_black = cv.threshold(img_black, 127, 255, cv.THRESH_BINARY)
    img_black = cv.medianBlur(img_black.astype(np.uint8), 5)
    return img_black

def average_rotation(path,out_path):  # path为读取img_mean.jpg的文件夹名称，如bin_resize，bin_rotation，bin_rotation2
    if not os.path.exists(out_path):#建立输出文件夹
        os.makedirs(out_path)
    #path(out_path).mkdir(parents=True, exist_ok=True)
    folder_list = os.listdir(path)  # 遍历子文件夹，生成子文件夹列表
    for folder in folder_list:  # 遍历文件夹
        new_path = os.path.join(path, folder)  # 子文件夹路径
        result = os.path.isdir(new_path)  # 判断输入文件夹下是否有文件夹
        #print(result)
        if str(result) == 'True':
            new_path = os.path.join(path, folder)  # 子文件夹路径
            new_output = os.path.join(out_path, folder)  # 生成文件夹的路径
            if not os.path.exists(new_output):  # 建立输出文件夹
                os.makedirs(new_output)

            jujuba_name_list = os.listdir(new_path)  # 生成文件名称列表
            img_average = average_pic(new_path)  # 生成该文件夹下所有图片的平均
            for jujuba_name in jujuba_name_list:  # 遍历子文件夹文件
                img = cv.imread(os.path.join(new_path, jujuba_name), cv.IMREAD_GRAYSCALE)  # 读入每张图片
                area_rotation = []  # 重叠面积列表
                matrix = [i for i in range(-25, 25)]  # 定义旋转角度
                for m in range(-25, 25):
                    img_rotated_by_alpha = rotation(m, img)  # 调用旋转函数，返回旋转后图片
                    img1, img2 = fill_boundary(img_average, img_rotated_by_alpha)  # 插值到相同大小
                    dst = cv.addWeighted(img1, 0.5, img2, 0.5, 0)  # 平均轮廓和旋转图叠加，各取1/2
                    ret, image = cv.threshold(dst, 250, 255, cv.THRESH_BINARY)  # 取其中白色的部分为重叠部分
                    close_Img1 = cv.medianBlur(image, 21)  # 中值滤波平滑边缘
                    canny_img = cv.Canny(close_Img1, 100, 200)
                    (cnts, add_image) = cv.findContours(canny_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 对重叠部分求轮廓
                    area = cv.contourArea(cnts[0])
                    area_rotation = np.append(area_rotation, area)  # 将面积输入到数组中

                area_array = np.array(area_rotation)
                maxindex = np.argmax(area_array)  # 最大重合面积的下标
                max_m = matrix[maxindex]  # 重合面积最大的旋转角度
                final_img_mean_rotation = rotation(max_m, img)  # 带入旋转函数
                cv.imwrite(os.path.join(new_output, jujuba_name), final_img_mean_rotation)  #

        if str(result) == 'False':
            jujuba_name_list = os.listdir(path)
            img_average = average_pic(path)

            for jujuba_name in jujuba_name_list:  # 遍历子文件夹文件
                img = cv.imread(os.path.join(path, jujuba_name), cv.IMREAD_GRAYSCALE)  # 读入每张图片
                area_rotation = []  # 重叠面积列表
                #print(path ,jujuba_name)
                matrix = [i for i in range(-25, 25)]  # 定义旋转角度
                for m in range(-25, 25):
                    img_rotated_by_alpha = rotation(m, img)  # 调用旋转函数，返回旋转后图片
                    img1, img2 = fill_boundary(img_average, img_rotated_by_alpha)  # 插值到相同大小
                    dst = cv.addWeighted(img1, 0.5, img2, 0.5, 0)  # 平均轮廓和旋转图叠加，各取1/2
                    ret, image = cv.threshold(dst, 250, 255, cv.THRESH_BINARY)  # 取其中白色的部分为重叠部分
                    close_Img1 = cv.medianBlur(image, 21)  # 中值滤波平滑边缘
                    canny_img = cv.Canny(close_Img1, 100, 200)
                    (cnts, add_image) = cv.findContours(canny_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 对重叠部分求轮廓
                    area = cv.contourArea(cnts[0])
                    area_rotation = np.append(area_rotation, area)  # 将面积输入到数组中

                area_array = np.array(area_rotation)
                maxindex = np.argmax(area_array)  # 最大重合面积的下标
                max_m = matrix[maxindex]  # 重合面积最大的旋转角度
                final_img_mean_rotation = rotation(max_m, img)  # 带入旋转函数
                cv.imwrite(os.path.join(out_path, jujuba_name), final_img_mean_rotation)  # 保存图片
            break

