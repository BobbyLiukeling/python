# -*- coding: utf-8 -*-
# @Time : 2021/12/24 0024 16:36
# @Author : Bobby_Liukeling
# @File : generate_graph.py


import torch
from torch_geometric.data import InMemoryDataset, download_url

from torch_geometric.data import Data
from rdkit.Chem import AllChem

from torch_geometric.datasets import QM9,TUDataset
from rdkit import Chem
import os
import numpy as np
import copy
import numpy as np


def process(path):





    edge_index = torch.tensor([[0, 1, 1, 2],
                               [1, 0, 2, 1]], dtype=torch.long)

    # 每个节点的特征：从0号节点开始。。
    x = torch.tensor([[-1], [0], [1]], dtype=torch.float)
    # 每个节点的标签：从0号节点开始-两类0，1
    y = torch.tensor([0, 1, 0])

    data = Data(x=x, edge_index=edge_index, y=y)
    # 放入datalist
    data_list = []
    data_list.append(data)

    edge_index = torch.tensor([[0, 1, 1, 2,3],
                               [1, 0, 2, 1,4]], dtype=torch.long)

    # 每个节点的特征：从0号节点开始。。
    x = torch.tensor([[-1], [0], [1],[1],[1]], dtype=torch.float)
    # 每个节点的标签：从0号节点开始-两类0，1
    y = torch.tensor([0, 1, 0,0,0])

    data = Data(x=x, edge_index=edge_index, y=y)
    # 放入datalist
    data_list.append(data)
    # data_list  = [data]

    # if self.pre_filter is not None:
    #     data_list = [data for data in data_list if self.pre_filter(data)]
    #
    # if self.pre_transform is not None:
    #     data_list = [self.pre_transform(data) for data in data_list]
    #
    # data, slices = self.collate(data_list)
    # torch.save((data, slices), self.processed_paths[0])

    # torch.save(data_list)


    np.save(path,data_list)




if __name__ =='__main__':
    path = r"data.npy"
    # process(path)


    """测试"""
    # b = MyOwnDataset("try")

    b = np.load(path,allow_pickle=True)
    # print(b)
    print(b[0])
    print("*"*10)
    print(b[0][0])

    print("*"*10)
    print(type(b[0][0]))

    print("*"*10)
    print(b[0][0][0])
    print("*"*10)
    print(b[0][0][1])




