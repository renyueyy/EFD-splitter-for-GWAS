def main():
    """
    主体函数：目的是对所有代码进行打包，展示所有功能
    显示功能界面
    :return:
    """
    print('Please choose--------------')
    print('1.picture division图片分割')
    print('2.find contour获得轮廓')
    print('3.resize面积均一')
    print('4.rotation basid on average根据平均轮廓旋转矫正方向')
    print('5.get average获得平均轮廓')
    print('6.rotation basid on symmetric根据对称性旋转矫正方向')
    print('7.efd求傅立叶系数')
    print('8.reconstruction傅立叶系数重建轮廓')
    print('9.area ratio获得重合面积比')
    print('10.exist')
    print('-'*20)
    return

#系统不退出，循环执行，直到选择6，才会退出系统
while True:
    #显示功能界面
    main()
    #输入选择的功能
    function = int(input('choose the function you want(1-10):'))
    
    #功能匹配
    #当选择功能1：图片分割
    if function == 1:
        import division
        input_path = input('input the route of origin picture:')
        output_path = input('input the route of output picture:')
        background_color = input('choose background color white,black or other(w/b/o):')
        if background_color == 'w':
            division.white_division(input_path, output_path)
        elif background_color =='b':
            division.black_division(input_path, output_path)
        elif background_color =='o':
            division.black_division(input_path, output_path)

    # 当选择功能2：轮廓提取
    elif function == 2:
        option = input('if you want to resize your pics in the same area:y/n')
        background = input('choose the background of your pics(b/w/o):')

        if option == 'n':
            if background == "b":
                import contours
                input_path = input('input the route of origin picture:')
                output_path = input('input the route of output picture:')
                contours.black_background(input_path, output_path)
            elif background == "w":
                import contours
                input_path = input('input the route of origin picture:')
                output_path = input('input the route of output picture:')
                contours.white_background(input_path, output_path)
            elif background == "o":
                import contours
                input_path = input('input the route of origin picture:')
                output_path = input('input the route of output picture:')
                contours.other_background(input_path, output_path)
        elif option == 'y':
            import resize
            input_path = input('input the route of origin picture:')
            output_path = input('input the route of output picture:')
            average_area = input('input the average area of output picture:')
            resize.black_background_resize(input_path, output_path,average_area)

    #当选择功能3，面积均一化
    elif function ==3:
        import resize
        input_path = input('input the route of origin picture:')
        output_path = input('input the route of output picture:')
        average_area = int(input('input the average area of output picture:'))
        resize.resize(input_path, average_area, output_path)

    # 当选择功能4，图片根据均值旋转，进行角度矫正
    elif function == 4:
        import overlap_rotation as ra
        input_path = input('input the route of origin picture:')
        output_path = input('input the route of output picture:')
        ra.average_rotation(input_path,output_path)

    # 当选择功能5，获得多张图片的平均轮廓
    elif function == 5:
        import average
        input_path = input('input the route of origin picture:')
        output_path = input('input the route of output picture:')
        average.average_pic(input_path,output_path)

    # 当选择功能6，根据对称性矫正方向
    elif function == 6:
        import mean_rotation as mr
        input_path = input('input the route of origin picture:')
        output_path = input('input the route of output picture:')
        mr.main(input_path,output_path)

    # 当选择功能7，求10级傅立叶系数
    elif function == 7:
        import efd
        input_path = input('input the route of origin picture:')
        output_path = input('input the route of output csv:')
        efd.efd_batch(input_path,output_path)

    # 当选择功能8，根据傅立叶系数轮廓重建
    elif function == 8:
        import contours_reconstruction as cr
        input_path = input('input the route of origin picture:')
        output_path = input('input the route of output picture:')
        cr.contour_reconstruction_batch_imgsave(input_path, output_path)

    # 当选择功能9，求重建轮廓和原图片的重叠百分比
    elif function == 9:
        import contours_reconstruction as cr
        input_path = input('input the route of origin picture:')
        output_path = input('input the route of output csv:')
        cr.overlape(input_path,output_path)
        #cr.percent(input_path,output_path)

    # 当选择功能10：退出系统
    elif function == 10:
        exist_glag = input('are you sure to exist? y/n:')
        if exist_glag=='y':
            break
        else:
            main()

    else:
        main()