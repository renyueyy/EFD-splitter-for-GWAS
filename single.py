import os
import numpy as np
import pandas as pd


def get_single_parameters(name, n, input):  # name为品种图片名字，如1-1(L1-1).jpg，n为要获取的参数为1-20
    #coeffs_path = os.path.join('./rsz_images', name, 'efd.csv')
    coeffs_path = input + f'/{name}'#输入文件所在文件夹
    coeffs = np.loadtxt(coeffs_path, delimiter=',')
    coeffs = coeffs.reshape((-1))
    return coeffs[n - 1]


def parameters_conversion(parameters):  # parameters为参数名称，如a1，b1，c1等
    n = 4 * (eval(parameters[1]) - 1) + ord(parameters[0]) - 96
    return n


def create_single_parameters_csv(parameters,path,input):
    """
    :param parameters: 参数名称，如a1，b1，c1等
    :param path: output path
    :param input: input path
    :return:
    """
    n = parameters_conversion(parameters)
    name_list = os.listdir(input)
    single_parameters_list = []
    for name in name_list:
        new_name = name.split('(')
        single_parameters_list.append([new_name, get_single_parameters(name, n, input)])
    single_parameters_array = np.array(single_parameters_list)
    single_parameters_df = pd.DataFrame(single_parameters_array, columns=['ID', f'{parameters}'])
    parameters_file_path = path#输出文件文件夹
    if not os.path.exists(parameters_file_path):
        os.makedirs(parameters_file_path)
    parameters_csv_path = os.path.join(parameters_file_path, f'{parameters}.csv')
    single_parameters_df.to_csv(parameters_csv_path, index=False)


def create_batch_parameters_csv(input,output):
    #path = "/Volumes/renyue-2T_A/my_project/simulation/norm/edf/"#输入文件所在文件夹
    path = output
    parameters_list = []
    for i in range(1, 11):
        for j in range(97, 101):
            parameters_list.append(f'{chr(j)}{i}')
    for parameters in parameters_list:
        create_single_parameters_csv(parameters,path,input)