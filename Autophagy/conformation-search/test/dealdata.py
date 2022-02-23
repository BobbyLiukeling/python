# -*- coding: utf-8 -*-
# @Time : 2021/10/29 0029 16:14
# @Author : Bobby_Liukeling
# @File : dealdata.py

import pandas as pd
import pdb

data = open(r'smiles.txt')
res = []
for i in data:
    # pdb.set_trace()
    res.append(i.strip('\n'))
# pdb.set_trace()
save = pd.DataFrame(columns=['smiles'], index = None, data=list(res)) #columns列名，index索引名，data数据

save.to_csv("smiles.csv",index=False)
