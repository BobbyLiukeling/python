# # -*- coding: utf-8 -*-
# # @Time : 2021/12/19 0019 10:13
# # @Author : Bobby_Liukeling
# # @File : molecule_generate_graph.py
#
# import torch
# from torch_geometric.data import Data
# from rdkit.Chem import AllChem
# from rdkit import Chem
# import os
#
# list_atom = {"C":0,"N":1, "O":2,"F":3}#对原子进行编码
#
# # path = 'delH_dsgdb9nsd_000009.pdb'
# path = "delH_dsgdb9nsd_051740.pdb"
# mol = AllChem.MolFromPDBFile(path)
#
# print('\t'.join(['id', 'num', 'symbol', 'degree', 'charge', 'hybrid']))
# atom_list = []
#
# for atom in mol.GetAtoms():
#     temp = []
#     # temp.append(atom.GetAtomicNum())
#     atom_num = atom.GetAtomicNum() #原子编号
#     pos = mol.GetConformer().GetAtomPosition(atom.GetIdx()) #原子坐标
#     print(atom.GetIdx(), end='\t')
#     print(atom.GetAtomicNum(), end='\t')
#     print(atom.GetSymbol(), end='\t')
#     print(atom.GetDegree(), end='\t')
#     print(atom.GetFormalCharge(), end='\t')
#     print(atom.GetHybridization(),end='\t')
#     print([x.GetIdx() for x in atom.GetNeighbors()],end='\t') #，与哪个原子相连接，但不能得出双键
#     x,y,z = mol.GetConformer().GetAtomPosition(atom.GetIdx())
#     print(x,y,z)
#
#
# print('\t'.join(['id', 'type', 'double', 'aromic', 'conjug', 'ring', 'begin', 'end']))
# for bond in mol.GetBonds():
#
#     print(bond.GetIdx(), end='\t')
#     print(bond.GetBondType(), end='\t')
#     print(bond.GetBondTypeAsDouble(), end='\t')
#     print(bond.GetIsAromatic(), end='\t')
#     print(bond.GetIsConjugated(), end='\t')
#     print(bond.IsInRing(), end='\t')
#     print(bond.GetBeginAtomIdx(), end='\t')
#     print(bond.GetEndAtomIdx())
#
# # # shape = [num_nodes, num_node_features]
# #
# # #C, O, N, F,一共只有这四种原子
# #
# # x = torch.tensor([[2,1], [5,6], [3,7], [12,0]]) #顶点属性向量
# # y = torch.tensor([0, 1, 0, 1]) #顶点label标签
# #
# #
# #
# # #边之间的连接关系
# # edge_index = torch.tensor([[0, 1, 2, 0, 3],
# #                            [1, 0, 1, 3, 2]])
# #
# # #边属性
# edge_attr = []  #这个和edge_index一一对应就好了
# #
# #
# # # pos : N x 3 的矩阵，用于表示上述图形当中的所有的Point的坐标
# # #face : 3 x [公式] 的矩阵，对矩阵当中的每一列，用于表示哪三个点可以构成一个“face，face就是面
# #
# # data = Data(x=x, y=y, edge_index=edge_index, edge_attr = edge_attr)
# # data
#
# '''
# Data(x=[4, 2], edge_index=[2, 5], y=[4])
# 说明有向边有5条、节点有4个、每个节点有两个特征
# '''

import sys  # 将输出信息写到日志中

log_print = open('Defalust.log', 'w')
sys.stdout = log_print
sys.stderr = log_print

print("test")