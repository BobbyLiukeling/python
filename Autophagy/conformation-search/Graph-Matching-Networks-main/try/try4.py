# -*- coding: utf-8 -*-
# @Time : 2022/2/3 0003 0:21
# @Author : Bobby_Liukeling
# @File : try4.py

import os,pdb
import pandas as pd
from pandas import Series
path = 'C:\\Users\\Administrator\\Desktop\\IVH_3d-上调基因配受体·20220202\\'#文件夹目录
files= os.listdir(path) #得到文件夹下的所有文件名称
data = pd.DataFrame(list(range(40)),columns=["temp"]) # 构建文件
for file in files:
    file_path = path+file #获得路径
    temp = pd.read_excel(file_path) #读取数据
    column_name = file.split("→")[0]+'_'+file.split("→")[1].split('.')[0] #获得文件名
    data[column_name] = temp['LR'] #添加数据
data = data.drop('temp',axis=1) #删除构建数据
data = data.dropna(axis=0,how='all')  #删除全空行
data.to_csv("day7.csv")


