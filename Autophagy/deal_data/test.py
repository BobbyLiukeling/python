# -*- coding: utf-8 -*-
# @Time : 2021/7/6 0006 9:57
# @Author : Bobby_Liukeling
# @File : test.py

import pandas as pd
import pdb

path = 'Acc_data.xlsx'



data_old = pd.read_excel('autophagy-GO-treat1.xls')['Acc(id)']

data_old = list(data_old)

with open("miss_data.txt",'r') as f:
    data_nan = f.read()
    f.close()
data_nan = data_nan.split(',')
pdb.set_trace()
data_pro = pd.read_excel(path)['AccId']
# pdb.set_trace()
data_pro = list(data_pro)

data_new = data_pro+data_nan
data_drop = set(data_new)-set(data_old)
data_new = set(data_new)-data_drop


pdb.set_trace()
wrong = set(data_old)-set(data_new)
# pdb.set_trace()
len(set(data_old))
len(set(data_new))