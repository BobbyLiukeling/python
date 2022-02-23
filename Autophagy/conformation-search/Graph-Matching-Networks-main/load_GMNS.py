# -*- coding: utf-8 -*-
# @Time : 2021/12/18 0018 19:23
# @Author : Bobby_Liukeling
# @File : load_GMNS.py

# -*- coding: utf-8 -*-
# @Time : 2021/12/18 0018 16:55
# @Author : Bobby_Liukeling
# @File : train_GMNS.py

from evaluation import compute_similarity, auc
from loss import pairwise_loss, triplet_loss
from utils import *
from configure import *
import numpy as np
import torch.nn as nn
import collections
import time
import os

import pdb

# Set GPU
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
use_cuda = torch.cuda.is_available()  # 查看cuda是否可用
device = torch.device('cuda:0' if use_cuda else 'cpu')  # 指定设备

# Print configure
config = get_default_config()
# for (k, v) in config.items(): # 查看设置参数
#     print("%s= %s" % (k, v)

#Set random seeds，以保证相同的输入，能输出相同的结果来
# seed = config['seed']  # seed = 8
# random.seed(seed)  # 设定随机种子
# np.random.seed(seed + 1)  # 设定随机种子
# torch.manual_seed(seed + 2)  # 设置CPU生成随机数的种子
# torch.backends.cudnn.deterministic = False
# torch.backends.cudnn.benchmark = True

# 加载或构建数据集模型
training_set, validation_set = build_datasets(config)  # 设置训练集测试集参数

# 生成固定大小的图

training_data_iter = training_set.pairs(config['training']['batch_size'])
# 每次取的是打包好的20对图的tuple 数据
first_batch_graphs, _ = next(training_data_iter)  # 这边可以一直调用数据，yield和next配合使用何以无限循环调用数据

node_feature_dim = first_batch_graphs.node_features.shape[-1]  # 顶点特征维度
edge_feature_dim = first_batch_graphs.edge_features.shape[-1]  # 边特征维度

'''
①先送进GraphEncoder前向，也即将两个_features分别通过两个MLP，输出node_features, edge_features尺寸由分别的hidden_sizes决定，
②五层prop层，每个方向是一层MLP接ReLu激活后再接一个MLP
③最后通过aggregator层整合节点信息
'''


model, optimizer = build_model(config, node_feature_dim, edge_feature_dim)  # 定义模型和优化器
model.to(device)  # 将模型送到设备中
for param_tensor in model.state_dict():
    print(param_tensor, "\t", model.state_dict()[param_tensor].size())
path = 'model_GMNs' + '.ckpt'
checkpoint = torch.load(path)
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
loss = checkpoint['loss']
accumulated_metrics = collections.defaultdict(list)  # 设置默认的list类型accumulated_metrics

training_n_graphs_in_batch = config['training']['batch_size']

training_n_graphs_in_batch *= 2  # 两两比对图的张数


#开始预测
model.eval()
batch = next(training_data_iter)  # 每个batch都是20对图（相似和不相似），以及labels
    # 两两图之间的比对
node_features, edge_features, from_idx, to_idx, graph_idx, labels = get_graph(batch)  # 从图中获取数据
labels = labels.to(device)  # 将属性送到设备中等待训练

#预测值
graph_vectors = model(node_features.to(device), edge_features.to(device), from_idx.to(device), to_idx.to(device),
                      graph_idx.to(device), training_n_graphs_in_batch)  # 将数据放到模型中开始训练 这是 predict_value，

x, y = reshape_and_split_tensor(graph_vectors, 2)
loss_score = pairwise_loss(x, y, labels,
                         loss_type=config['training']['loss'],
                         margin=config['training']['margin'])

print(loss_score)
# print(loss_score[0])
# print(loss_score.data.cpu().numpy())

#20对图的预测结果，数字越小预测结果越好，之后再修改
prediction = loss_score.data.cpu().numpy().tolist()
#将预测结果从tensor转为array，并抽取结果
# prediction = loss_score.numpy()
a = 0

'''
        def load_checkpoint(path): 
            model = pytorch_cnn(num_classes).to('cpu')

            # Print model's state_dict
            print("Model's state_dict:")
            for param_tensor in model.state_dict():
                print(param_tensor, "\t", model.state_dict()[param_tensor].size())

            optimizer = optim.Adam(model.parameters(), lr=1e-3)    
            checkpoint = torch.load(path)
            model.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            epoch = checkpoint['epoch']
            loss = checkpoint['loss']


            return model, optimizer, epoch, loss

            model, optimizer, epoch, loss = load_checkpoint(path=path)

        '''
