# -*- coding: utf-8 -*-
# @Time : 2021/12/20 0020 15:09
# @Author : Bobby_Liukeling
# @File : try.py
# -*- coding: utf-8 -*-
# @Time : 2021/12/19 0019 10:13
# @Author : Bobby_Liukeling
# @File : molecule_generate_graph.py

import torch
from torch_geometric.data import Data
from rdkit.Chem import AllChem

from torch_geometric.datasets import QM9,TUDataset
from rdkit import Chem
import os
import numpy as np
import copy

def atomPDB_to_graph(path):
    '''
    对一张图进行编码
    :param path: pdb file path
    :return: torch_geometric 类型的图数据
    '''


    mol = AllChem.MolFromPDBFile(path)

    # 获取原子顶点属性
    atom_feature = []
    pos = [] #原子坐标信息
    for atom in mol.GetAtoms():
        temp = []
        # temp.append(atom.GetAtomicNum())
        atom_num = atom.GetAtomicNum()  # 原子编号
        x, y, z = mol.GetConformer().GetAtomPosition(atom.GetIdx())  # 原子坐标

        temp.append(atom_num)
        temp.extend([x, y, z])
        pos.append([x, y, z])
    atom_feature.append(temp)
    bond_feature_dict = {'SINGLE': 1, 'DOUBLE': 2, 'TRIPLE': 3}#三种键类型

    # 获取边属性，
    edge_index = []
    from_idx = []
    to_idx = []
    edge_feature = []  # 单键，双键、三键
    for bond in mol.GetBonds():
        from_idx.append(bond.GetBeginAtomIdx())
        to_idx.append(bond.GetEndAtomIdx())
        edge_feature.append(bond_feature_dict[str(bond.GetBondType())])
    #edge_index 表示的是有向图，所以边信息要进行double处理，变成无向图
    temp = copy.deepcopy(from_idx) #这里要用深拷贝
    from_idx.extend(to_idx)
    to_idx.extend(temp)
    edge_index.append(from_idx)
    edge_index.append(to_idx)
    edge_feature.extend(edge_feature)


    graph_data = Data(x=atom_feature, edge_index=edge_index, edge_attr=edge_feature,pos = pos)

    return graph_data


def pc_normalize(pc): #将数据标准化
    '''
    参考博客：https://blog.csdn.net/weixin_41496173/article/details/115330908
    :param pc:
    :return:
    '''
    l = pc.shape[0]
    centroid = np.mean(pc, axis=0)#求这个batch点云的均值
    pc = pc - centroid
    m = np.max(np.sqrt(np.sum(pc**2, axis=1)))#求这个batch点云的模的最大值
    pc = pc / m
    return pc




if __name__ == '__main__':
    path = 'delH_dsgdb9nsd_000009.pdb'
    pwd = os.getcwd()
    father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
    # path = "delH_dsgdb9nsd_051740.pdb"
    # F:\Code\Python\Autophagy\conformation - search\Graph - Matching - Networks - main\prework\xyz_changeto_pdb\xyz\pdb
    path = father_path+'/xyz_changeto_pdb/xyz/pdb/'+'delH_dsgdb9nsd_000009.pdb'

    graph_data = atomPDB_to_graph(path)
    print(graph_data.edge_index)