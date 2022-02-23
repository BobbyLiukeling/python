# -*- coding: utf-8 -*-
# @Time : 2021/11/29 0029 17:32
# @Author : Bobby_Liukeling
# @File : train_loader.py
import numpy as np
import pdb
data = np.load("qm9_eV.npz")
# for i in data:
#     try:
#         print("*"*15,i,"*"*15)
#         print(data[i].shape)
#         print(data[i][:5])
#
#     except:
#         pass


    # if i in ['id', 'N', 'Z', 'R']:
    #     print(type(data[i]))

# print(data['R'])

print(type(data))
print(data.files) #['R', 'N', 'Z', 'id', 'A', 'B', 'C', 'mu', 'alpha', 'homo', 'lumo', 'gap', 'r2', 'zpve', 'U0', 'U', 'H', 'G', 'Cv', 'meta']