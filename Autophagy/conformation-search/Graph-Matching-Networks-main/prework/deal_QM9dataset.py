# -*- coding: utf-8 -*-
# @Time : 2021/12/23 0023 17:06
# @Author : Bobby_Liukeling
# @File : deal_QM9dataset.py

import os.path as osp

import torch

from torch_geometric.datasets import QM9

from torch_geometric.data.data import Data
from torch_geometric.data import data
from torch_geometric.loader import DataLoader


path = osp.join(osp.dirname(osp.realpath(__file__)), '..', 'data', 'QM9')
dataset = QM9(path)

# DimeNet uses the atomization energy for targets U0, U, H, and G.
idx = torch.tensor([0, 1, 2, 3, 4, 5, 6, 12, 13, 14, 15, 11])
dataset.data.y = dataset.data.y[:, idx]

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') #设置设备
# 数据来了
print(dataset.data.keys)
# print(dataset.data.edge_attr.shape)
#130831

# print(type(dataset.data))

'''
['x', 'edge_attr', 'edge_index', 'z', 'idx', 'pos', 'name', 'y']
torch.Size([4883516, 4])
<class 'torch_geometric.data.data.Data'>
edge_attr:  torch.Size([4883516, 4])
edge_index:  torch.Size([4883516, 4])
y:  torch.Size([4883516, 4])
z:  torch.Size([4883516, 4])
idx:  torch.Size([4883516, 4])
edge_attr:  torch.Size([4883516, 4])
pos:  torch.Size([4883516, 4])
x: torch.Size([4883516, 4])
name: torch.Size([4883516, 4])
'''

print("slices:",dataset.slices['edge_attr'])
print("slices:",dataset.slices['edge_attr'][130832-1])
print("slices:",dataset.slices['edge_attr'].shape)
print("slices:",dataset.slices['edge_attr'].shape[0])

print("slices2:",dataset.slices['pos'].data[0])
print("slices2:",dataset.slices['pos'].T[0])
# print("slices2:",dataset.slices['pos'].item())




# print("edge_index: ",dataset.slices.edge_index.shape,dataset.data.edge_index[0])
# print("y: ",dataset.slices.y.shape,dataset.data.y[0])
# print("z: ",dataset.slices.z.shape,dataset.data.z[0])
# print("idx: ",dataset.slices.idx.shape,dataset.data.idx[0])
# print("edge_attr: ",dataset.slices.edge_attr.shape,dataset.data.edge_attr[0])
# print("pos: ",dataset.slices.pos.shape,dataset.data.pos[0])
# print("x:",dataset.slices.x.shape,dataset.data.x[0])
# print("name:",dataset.slices.name.shape,dataset.data.name[0])

# try:
#     print("name:",dataset.data.name.shape)
# except:
#     print("name is none")

print(type(dataset))

loader = DataLoader(dataset, batch_size=20)





a = 0