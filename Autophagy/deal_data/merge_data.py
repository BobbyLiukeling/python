# -*- coding: utf-8 -*-
# @Time : 2021/7/6 0006 0:39
# @Author : Bobby_Liukeling
# @File : merge_data.py

import pandas as pd
import pdb

df = pd.DataFrame(columns=["AccId","pro_type"])
for i in range(6):
    pdb.set_trace()
    temp = pd.read_csv("Acc_data{}.xlsx".format(i+1))
    df = df.append(temp,ignore_index=True)

# pdb.set_trace()
df.to_excel("Acc_data.xlsx")