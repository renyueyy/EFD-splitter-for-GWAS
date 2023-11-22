def main():
    """
    主体函数：目的是对所有代码进行打包，展示所有功能
    显示功能界面
    :return:
    """
    print('Please choose--------------')
    print('1.Picture division:')
    print('2.Find contours:')
    print('3.Resize:')
    print('4.Rotation based on average:')
    print('5.Get average contours:')
    print('6.Rotation based on symmetric：')
    print('7.Get EFDs:')
    print('8.Contour reconstruction for different level of EFDs:')
    print('9.Area ratio:')
    print('10.Statistical EFDs format:')
    print('11.Contour reconstruction for different genotypes:')
    print('12.Exit:')
    print('-'*20)
    return

#系统不退出，循环执行，直到选择11才会退出系统
while True:
    #显示功能界面
    main()
    #输入选择的功能
    function = int(input('choose the function you want(1-12):'))
    
    #功能匹配
    #当选择功能1：图片分割
    if function == 1:
        import division
        #print('#the "input_path" is the path of folder where images located')
        input_path = input('input the folder of origin picture:')
        output_path = input('input the folder of output picture:')
        background_color = input('choose background color, white,black or other(w/b/o):')
        if background_color == 'w':
            division.white_division(input_path, output_path)
        elif background_color =='b':
            division.black_division(input_path, output_path)
        elif background_color =='o':
            division.black_division(input_path, output_path)

    # 当选择功能2：轮廓提取
    elif function == 2:
        background = input('choose the background of your pics, white,black or other:white/black/other(w/b/o):')

        if background == "b":
            import contours
            input_path = input('input the folder of origin picture:')
            output_path = input('input the folder of output picture:')
            contours.black_background(input_path, output_path)

        elif background == "w":
                import contours
                input_path = input('input the folder of origin picture:')
                output_path = input('input the folder of output picture:')
                contours.white_background(input_path, output_path)

        elif background == "o":
                import contours
                input_path = input('input the folder of origin picture:')
                output_path = input('input the folder of output picture:')
                contours.other_background(input_path, output_path)

    #当选择功能3，面积均一化
    elif function ==3:
        import resize
        input_path = input('input the folder of origin picture:')
        output_path = input('input the route of output picture:')
        average_area = int(input('input the average area of output picture:'))
        resize.resize(input_path, average_area, output_path)

    # 当选择功能4，图片根据均值旋转，进行角度矫正
    elif function == 4:
        import overlap_rotation as ra
        #average_path = input('input the folder of average picture:')
        input_path = input('input the folder of origin picture:')
        output_path = input('input the route of output picture:')
        ra.average_rotation(input_path,output_path)

    # 当选择功能5，获得多张图片的平均轮廓
    elif function == 5:
        import average
        input_path = input('input the folder of origin picture:')
        output_path = input('input the route of output picture:')
        average.average_pic(input_path,output_path)

    # 当选择功能6，根据对称性矫正方向
    elif function == 6:
        import mean_rotation as mr
        input_path = input('input the folder of origin picture:')
        output_path = input('input the route of output picture:')
        direction = input('the direction of symmetry of the picture (horizontal/perpendicular):')
        mr.main(input_path,output_path,direction)

    # 当选择功能7，求10级傅立叶系数
    elif function == 7:
        import efd
        input_path = input('input the folder of origin picture:')
        output_path = input('input the route of output csv:')
        efd.efd_batch(input_path,output_path)

    # 当选择功能8，根据傅立叶系数轮廓重建
    elif function == 8:
        import contours_reconstruction as cr
        input_path = input('input the folder of origin picture:')
        output_path = input('input the route of output picture:')
        cr.contour_reconstruction_batch_imgsave(input_path, output_path)

    # 当选择功能9，求重建轮廓和原图片的重叠百分比
    elif function == 9:
        import contours_reconstruction as cr
        input_path = input('input the folder of origin picture:')
        output_path = input('input the route of output csv:')
        cr.overlape(input_path,output_path)
        #cr.percent(input_path,output_path)

    #整理参数为整个的表格
    elif function == 10:
        import single
        input_path = input('input the folder of tables:')
        output_path = input('input the route of output csv:')
        single.create_batch_parameters_csv(input_path,output_path)
        #cr.percent(input_path,output_path)

    #不同基因型的轮廓重建
    elif function == 11:
        import reconstruction as re
        input_path = input('input the route of genotype:')
        output_path = input('input the route of output folder:')
        re.contour_reconstruction_batch_imgsave(input_path,output_path)

    # 当选择功能13：退出系统
    elif function == 12:
        exist_glag = input('are you sure to exist? y/n:')
        if exist_glag=='y':
            break
        else:
            main()

    else:
        main()