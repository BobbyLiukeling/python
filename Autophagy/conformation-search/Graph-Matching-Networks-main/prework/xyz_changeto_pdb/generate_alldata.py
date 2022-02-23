# -*- coding: utf-8 -*-
# @Time : 2021/12/26 0026 21:03
# @Author : Bobby_Liukeling
# @File : generate_alldata.py

from torch_geometric.data import Data
import numpy as np
import os
import torch
import copy,pdb
from rdkit.Chem import AllChem
import time
import datetime

import sys   #将输出信息写到日志中

log_print = open('Defalust.log', 'w')
sys.stdout = log_print
sys.stderr = log_print


'''
将去氢的pdb文件全部转化为npy文件
'''





def process(path):
    files = os.listdir(path)
    graph_list = []

    i = 1

    start = time.time()

    for file in files:
        file = path+'/'+file
        mol = AllChem.MolFromPDBFile(file,sanitize=True,removeHs=True,flavor=0,proximityBonding=False)

        # 获取原子顶点属性
        atom_feature = []
        pos = []  # 原子坐标信息
        try:
            for atom in mol.GetAtoms():
                temp = []
                # temp.append(atom.GetAtomicNum())
                atom_num = atom.GetAtomicNum()  # 原子编号
                x, y, z = mol.GetConformer().GetAtomPosition(atom.GetIdx())  # 原子坐标

                temp.append(atom_num)
                temp.extend([x, y, z])
                pos.append([x, y, z])
            atom_feature.append(temp)
            bond_feature_dict = {'SINGLE': 0, 'DOUBLE': 1, 'TRIPLE': 2,'AROMATIC':3}  # 三种键类型

            # 获取边属性，
            edge_index = []
            from_idx = []
            to_idx = []
            edge_feature = []  # 单键，双键、三键
            for bond in mol.GetBonds():
                from_idx.append(bond.GetBeginAtomIdx())
                to_idx.append(bond.GetEndAtomIdx())
                edge_feature.append(bond_feature_dict[str(bond.GetBondType())])
            # edge_index 表示的是有向图，所以边信息要进行double处理，变成无向图
        except Exception as e:
            print(e)
            # print(AllChem.MolToSmiles(mol))
            # print(mol)
            print(file)
            # pdb.set_trace()

        # for atom in mol.GetAtoms():
        #     temp = []
        #     # temp.append(atom.GetAtomicNum())
        #     atom_num = atom.GetAtomicNum()  # 原子编号
        #     x, y, z = mol.GetConformer().GetAtomPosition(atom.GetIdx())  # 原子坐标
        #
        #     temp.append(atom_num)
        #     temp.extend([x, y, z])
        #     pos.append([x, y, z])
        # atom_feature.append(temp)
        # bond_feature_dict = {'SINGLE': 1, 'DOUBLE': 2, 'TRIPLE': 3}  # 三种键类型
        #
        # # 获取边属性，
        # edge_index = []
        # from_idx = []
        # to_idx = []
        # edge_feature = []  # 单键，双键、三键
        # for bond in mol.GetBonds():
        #     from_idx.append(bond.GetBeginAtomIdx())
        #     to_idx.append(bond.GetEndAtomIdx())
        #     edge_feature.append(bond_feature_dict[str(bond.GetBondType())])
        # # edge_index 表示的是有向图，所以边信息要进行double处理，变成无向图


        temp = copy.deepcopy(from_idx)  # 这里要用深拷贝
        from_idx.extend(to_idx)
        to_idx.extend(temp)
        edge_index.append(from_idx)
        edge_index.append(to_idx)
        edge_feature.extend(edge_feature)

        graph_data = Data(x=atom_feature, edge_index=edge_index, edge_attr=edge_feature, pos=pos)
        graph_list.append(graph_data)


        #计时

        if i%1000== 0:
            runtime = time.time()
            print('this is {}k run time is : {}'.format(i/1000,str(datetime.timedelta(seconds=runtime-start))))

        i = i+1

        # print(i,end='/n')


    np.save('last_data/all_nparry.npy', graph_list) #存储数据，位置：last_data/all_nparry.npy


if __name__ == '__main__':
    print("```````````````````````begin```````````````````")
    start = time.time()
    path = r"all_delH"
    process(path)

    end = time.time()
    print('totle run time is : ',str(datetime.timedelta(seconds=end-start)))
    print('``````````````````````end```````````````````````')

    """测试"""
    # b = MyOwnDataset("try")

    # b = np.load(path, allow_pickle=True)
    # # print(b)
    # print(b[0])
    # print("*" * 10)
    # print(b[0][0])
    #
    # print("*" * 10)
    # print(type(b[0][0]))
    #
    # print("*" * 10)
    # print(b[0][0][0])
    # print("*" * 10)
    # print(b[0][0][1])
