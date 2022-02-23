# -*- coding: utf-8 -*-
# @Time : 2021/12/6 0006 18:11
# @Author : Bobby_Liukeling
# @File : change.py

import os
import warnings,pdb
warnings.filterwarnings("ignore")
# path_xyz = 'xyz'
path_xyz = 'all_xyz'
path_pdb = 'pdb'
s = 'dsgdb9nsd'
files= os.listdir(path_xyz) #得到文件夹下的所有文件名称

pwd = os.path.dirname(os.path.realpath(__file__)) #当前文件夹下
os.chdir(pwd+"/"+path_xyz)  # 跳转到当前文件夹下

# for file in files: #遍历文件夹
#      if not os.path.isdir(file):
#           # pdb.set_trace()
#           strings = "obabel dsgdb9nsd_00000{}.xyz -ixyz -opdb -O {}/dsgdb9nsd_00000{}.pdb".format(i,path_pdb,i)
#           os.system(strings)
#           i = i+1
#

# os.system("source ~/.bashrc")
# os.system("conda activate auto")


for file in files: #遍历文件夹
     if not os.path.isdir(file.endswith("xyz")):
          string =  file.split('_')[-1].split('.')[0]
          strings = "obabel dsgdb9nsd_{}.xyz -ixyz -opdb -O {}/dsgdb9nsd_{}.pdb".format(string,path_pdb,string)
          # print(strings)
          try:
               os.system(strings)
               # print(file)
               # print("ok!")
          except Exception as e :
               pdb.set_trace()
# path = 'dsgdb9nsd_128990.xyz'
# obabel dsgdb9nsd_000001.xyz -ixyz -opdb -O dsgdb9nsd_000001.pdb
               pass
               # print(file)



