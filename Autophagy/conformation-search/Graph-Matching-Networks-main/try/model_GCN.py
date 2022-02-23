# -*- coding: utf-8 -*-
# @Time : 2021/11/17 0017 14:58
# @Author : Bobby_Liukeling
# @File : model_GCN.py
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.datasets import Planetoid
import torch_geometric.nn as pyg_nn
import pandas as pd
import numpy as np
import pdb

#1、准备数据
def get_data(folder="node_classify/cora", data_name="ind.cora.tx"):
    """
        :param folder:保存数据集的根目录。
        :param data_name:数据集的名称
        :return:返回的是一个对象，就是PyG文档里的Data对象，它有一些属性，如 data.x、data.edge_index等
    """
    # dataset = Planetoid(root=folder,name=data_name)
    dataset = np.load("ind.cora.tx")
    return dataset

#2、定义模型
class CraphCNN(nn.Module):
    def __init__(self,in_c,hid_c,out_c):
        super(CraphCNN,self).__init__() #表示继承nn.Moudle
        # 下面这个就是前面讲的GCN，参数只有输入和输出，定义了两层的GCN.
        self.conv1 = pyg_nn.GCNConv(in_channels=in_c, out_channels=hid_c)
        self.conv2 = pyg_nn.GCNConv(in_channels=hid_c, out_channels=out_c)

    #前向传播
    def forward(self,data):
        # data.x  data.edge_index
        x = data.x  # [N, C], C为特征的维度
        edge_index = data.edge_index  # [2, E], E为边的数量
        hid = self.conv1(x=x, edge_index=edge_index)  # [N, D], N是节点数量，D是第一层输出的隐藏层的维度
        hid = F.relu(hid)
        out = self.conv2(x=hid, edge_index=edge_index)  # [N, out_c], out_c就是定义的输出，比如分成几类就是几，这里是7
        out = F.log_softmax(out, dim=1)  # [N, out_c],表示输出
        return out


#自定义图卷积
class MyGCN(nn.Module):
    pass


#搭建训练框架
def main():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # 配置GPU
    cora_dataset = get_data()

    #实例化模型
    my_net = GraphCNN(in_c=cora_dataset.num_node_features, hid_c=13, out_c=cora_dataset.num_classes)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu") #准备设备

    my_net = my_net.to(device)  # 模型送入设备
    data = cora_dataset[0].to(device)  # 数据送入设备，也就是一张图

    # 第三步：定义损失函数和优化器
    optimizer = torch.optim.Adam(my_net.parameters(), lr=1e-3)  # 优化器

    # 第四步：训练
    # model train,这个train就是说归一化等可以重复使用，而设置成eval则就不行了，表示测试
    my_net.train()
    for epoch in range(200):
        optimizer.zero_grad()  # 每次缓存之后清零,不然梯度会累加

        output = my_net(data)  # 预测结果

        loss = F.nll_loss(output[data.train_mask], data.y[data.train_mask])  # 意思就是只取训练集
        loss.backward()
        print("epoch:", epoch + 1, loss.item())
        optimizer.step()  # 优化器

    # model test，模型测试
    my_net.eval()
    _, prediction = my_net(data).max(dim=1)
    target = data.y
    test_correct = prediction[data.test_mask].eq(target[data.test_mask]).sum().item()
    test_number = data.test_mask.sum().item()

    print("Accuracy of Test Samples:{}%".format(100 * test_correct / test_number))

if __name__ == "__main__":
    main()














