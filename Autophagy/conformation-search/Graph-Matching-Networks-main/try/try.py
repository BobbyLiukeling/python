# -*- coding: utf-8 -*-
# @Time : 2022/2/2 0002 13:40
# @Author : Bobby_Liukeling
# @File : try.py


import pandas as pd
import numpy as np
import pdb
from pandas import Series
# data = pd.read_csv("try.csv")

# columns = data.columns
# for column in columns:
#     data[column]
#
# data['VL_CA1'].append()
# pdb.set_trace()


def getpart(path):
    temp = []
    with open (path,'r') as f:
        lines = f.readlines()
        for line in lines:
            if line == '\n':
                continue
            temp.append(line.split('(')[-1].split(')')[0].replace(" ",""))
    # pdb.set_trace()
    return list(set(temp))

            # pdb.set_trace()
# getpart('try.txt')
#
# s = ['VL_CA1', 'VL_CA3', 'cpd_HYL', 'cpd_MB', 'fxs_HYL', 'fxs_MB', 'HYL_TH',
#        'MB_TH', 'TH_CA1', 'TH_CA3', 'VL_cpd', 'VL_fxs', 'I_RSP', 'I_V-Via-Vib',
#        'V-VIa-Vib_II-III-IV', 'VL_I', 'CA1-DG']
column = 'I_RSP'
temp = getpart('try.txt')

data = pd.read_csv('try.csv')
# data[column] = temp
columns = data.columns
# pdb.set_trace()
if column not in columns:
    data[column] = Series(temp)
else:
    temp.extend(data[column].tolist())
    nan = temp[-1]
    temp = set(temp)
    try:
        temp.remove('\n')
    except:
        pass
    temp.remove(nan)
    data[column] = Series(list(temp))
data.to_csv('try.csv',index=None)


# "UP" + "" + path.split("\\")[-1] + "" + column + "" + i + ".csv"