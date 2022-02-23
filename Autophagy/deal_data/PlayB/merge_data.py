# -*- coding: utf-8 -*-
# @Time : 2021/7/6 0006 0:39
# @Author : Bobby_Liukeling
# @File : merge_data.py

import pandas as pd
import pdb

# a = pd.read_excel("Acc_data1.xlsx")
# pdb.set_trace()

df = pd.DataFrame(columns=["AccId","pro_type"])
for i in range(3):
    path = "Acc_data{}.xlsx".format(i+1)
    temp = pd.read_excel(path)
    df = df.append(temp,ignore_index=True)

# pdb.set_trace()
df.to_excel("Acc_data.xlsx")