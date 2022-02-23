# -*- coding: utf-8 -*-
# @Time : 2021/12/21 0021 20:30
# @Author : Bobby_Liukeling
# @File : new_utils.py

import torch
from torch_geometric.data import Data
from rdkit.Chem import AllChem

from torch_geometric.datasets import QM9,TUDataset
from rdkit import Chem
import os
import numpy as np
import copy

def atomPDB_to_graph():
    '''
    对一张图进行编码
    :param path: pdb file path
    :return: torch_geometric 类型的图数据
    '''

    pwd = os.getcwd()
    father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
    # path = "delH_dsgdb9nsd_051740.pdb"
    # F:\Code\Python\Autophagy\conformation - search\Graph - Matching - Networks - main\prework\xyz_changeto_pdb\xyz\pdb
    path = father_path+'/xyz_changeto_pdb/xyz/pdb/' #数据存放位置
    key = "delH"

    for file in os.listdir(path):
        if str(file).startswith(key):
            mol = AllChem.MolFromPDBFile(path)

            # 获取原子顶点属性
            atom_feature = []
            pos = []  # 原子坐标信息
            for atom in mol.GetAtoms():
                temp = []
                # temp.append(atom.GetAtomicNum())
                atom_num = atom.GetAtomicNum()  # 原子编号
                x, y, z = mol.GetConformer().GetAtomPosition(atom.GetIdx())  # 原子坐标

                temp.append(atom_num)
                temp.extend([x, y, z])
                pos.append([x, y, z])
            atom_feature.append(temp)
            bond_feature_dict = {'SINGLE': 1, 'DOUBLE': 2, 'TRIPLE': 3}  # 三种键类型

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
            temp = copy.deepcopy(from_idx)  # 这里要用深拷贝
            from_idx.extend(to_idx)
            to_idx.extend(temp)
            edge_index.append(from_idx)
            edge_index.append(to_idx)
            edge_feature.extend(edge_feature)

            graph_data = Data(x=atom_feature, edge_index=edge_index, edge_attr=edge_feature, pos=pos)

            yield graph_data
        else:
            pass

    # string.find(file, key) != -1



