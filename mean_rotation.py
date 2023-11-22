import cv2 as cv
import numpy as np
import os

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

def area(image_origin,image_end):
    dst = cv.addWeighted(image_origin, 0.5, image_end, 0.5, 0)  # 平均轮廓和旋转图叠加，各取1/2
    ret, image = cv.threshold(dst, 250, 255, cv.THRESH_BINARY)  # 取其中白色的部分为重叠部分
    close_Img = cv.medianBlur(image, 21)  # 中值滤波平滑边缘
    (cnts, add_image) = cv.findContours(close_Img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 对重叠部分求轮廓
    area = 0  # 求轮廓面积即为重叠面积
    for n in cnts:
        area += cv.contourArea(n)
    return area

class BBox(object):
    def __init__(self, bbox):
        self.left = bbox[0]
        self.top = bbox[1]
        self.right = bbox[2]
        self.bottom = bbox[3]

def rotation(m, img_2):
    """
    旋转图片
    m：旋转角度
    img_2：需要旋转的图片
    :return:旋转一定角度后的图片
    """
    h, w = img_2.shape
    box = [0, 0, w, h]
    bbox = BBox(box)
    degree = m  # 旋转角度
    center = ((bbox.left + bbox.right) / 2, (bbox.top + bbox.bottom) / 2)
    rot_mat = cv.getRotationMatrix2D(center, degree, 1)
    img_rotated_by_alpha = cv.warpAffine(img_2, rot_mat, (img_2.shape[1], img_2.shape[0]))
    # cv.imshow("a", img_rotated_by_alpha)
    return img_rotated_by_alpha

def overlap_area(image):
    area_rotation = []
    matrix = [i for i in range(-25, 25)]
    for m in range(-25, 25):
        img_rotated_by_alpha = rotation(m, image)  # 调用旋转函数，返回旋转后图片
        #img1, img2 = fill_boundary(image, img_rotated_by_alpha)  # 插值到相同大小
        flipped = cv.flip(img_rotated_by_alpha, 0)
        cv.imshow("flipped", flipped)
        #area = area(flipped, img_rotated_by_alpha)
        dst = cv.addWeighted(flipped, 0.5, img_rotated_by_alpha, 0.5, 0)  # 平均轮廓和旋转图叠加，各取1/2
        cv.imshow("dst",dst)

        ret, img = cv.threshold(dst, 250, 255, cv.THRESH_BINARY)  # 取其中白色的部分为重叠部分
        cv.imshow("image",img)
        close_Img = cv.medianBlur(img, 21)  # 中值滤波平滑边缘
        (cnts, add_image) = cv.findContours(close_Img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 对重叠部分求轮廓
        area = 0  # 求轮廓面积即为重叠面积
        #cv.waitKey()
        for n in cnts:
            area += cv.contourArea(n)

        area_rotation = np.append(area_rotation, area)  # 将面积输入到数组中
    arr_aa = np.array(area_rotation)
    #print(arr_aa)
    maxindex = np.argmax(arr_aa)  # 最大重合面积的下标
    max = matrix[maxindex]  # 重合面积最大的旋转角度
    final_img = rotation(max, image)  # 利用旋转角度和原图，带入旋转函数，生成旋转图
    return max

def main(input_path,output_path,direction):
    if not os.path.exists(output_path):#建立输出文件夹
        os.makedirs(output_path)
    name_list = os.listdir(input_path)
    if direction== "horizontal":
        for name in name_list:
            image = cv.imread(os.path.join(input_path, name), cv.IMREAD_GRAYSCALE)
            max = overlap_area(image)
            final_img = rotation(max, image)
            cv.imwrite(os.path.join(output_path, name), final_img)

    elif direction == "perpendicular":
        for name in name_list:
            image = cv.imread(os.path.join(input_path, name), cv.IMREAD_GRAYSCALE)
            image_rotation1 = cv.rotate(image, cv.ROTATE_90_COUNTERCLOCKWISE)#逆时针旋转90°，让图片变为水平对称
            max = overlap_area(image_rotation1)
            final_img = rotation(max, image_rotation1)
            rotated_image = cv.rotate(final_img, cv.ROTATE_90_CLOCKWISE)#顺时针旋转90°，让图片变为垂直对称，与原始图片方向一致
            cv.imwrite(os.path.join(output_path, name), rotated_image)