# -*- coding: utf-8 -*-
# @Time : 2022/1/18 0018 19:18
# @Author : Bobby_Liukeling
# @File : sdf_to_pdb.py


import os
import warnings,pdb

pwd = os.path.dirname(os.path.realpath(__file__)) #当前文件夹下
files = os.listdir(pwd) #得到文件夹下的所有文件名称
os.chdir(pwd)  # 跳转到当前文件夹下
for file in files: #遍历文件夹
     if file.endswith("sdf"):
          string =  file.split('_')[-1].split('.')[0]
          strings = "obabel {}.sdf -isdf -opdb -O {}.pdb".format(string,string)
          try:
               os.system(strings)
          except Exception as e :
               pdb.set_trace()
               pass
