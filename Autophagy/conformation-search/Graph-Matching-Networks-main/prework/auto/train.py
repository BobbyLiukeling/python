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
use_cuda = torch.cuda.is_available() #查看cuda是否可用
device = torch.device('cuda:0' if use_cuda else 'cpu') #指定设备

# Print configure
config = get_default_config()
# for (k, v) in config.items(): # 查看设置参数
#     print("%s= %s" % (k, v)

# Set random seeds，以保证相同的输入，能输出相同的结果来
seed = config['seed'] #seed = 8
random.seed(seed) #设定随机种子
np.random.seed(seed + 1) #设定随机种子
torch.manual_seed(seed + 2) #设置CPU生成随机数的种子
torch.backends.cudnn.deterministic = False
torch.backends.cudnn.benchmark = True

#加载或构建数据集模型
training_set, validation_set = build_datasets(config) #设置训练集测试集参数

#生成固定大小的图
if config['training']['mode'] == 'pair': #两两比对
    training_data_iter = training_set.pairs(config['training']['batch_size'])
    #每次取的是打包好的20对图的tuple 数据
    first_batch_graphs, _ = next(training_data_iter) #这边可以一直调用数据，yield和next配合使用何以无限循环调用数据
else:
    training_data_iter = training_set.triplets(config['training']['batch_size'])
    first_batch_graphs = next(training_data_iter)

node_feature_dim = first_batch_graphs.node_features.shape[-1]#顶点特征维度
edge_feature_dim = first_batch_graphs.edge_features.shape[-1]#边特征维度

'''
①先送进GraphEncoder前向，也即将两个_features分别通过两个MLP，输出node_features, edge_features尺寸由分别的hidden_sizes决定，
②五层prop层，每个方向是一层MLP接ReLu激活后再接一个MLP
③最后通过aggregator层整合节点信息
'''

model, optimizer = build_model(config, node_feature_dim, edge_feature_dim) #定义模型和优化器
model.to(device) #将模型送到设备中

accumulated_metrics = collections.defaultdict(list) #设置默认的list类型accumulated_metrics


training_n_graphs_in_batch = config['training']['batch_size']
if config['training']['mode'] == 'pair':
    training_n_graphs_in_batch *= 2 #两两比对图的张数
elif config['training']['mode'] == 'triplet':
    training_n_graphs_in_batch *= 4
else:
    raise ValueError('Unknown training mode: %s' % config['training']['mode'])

t_start = time.time() #开始时间
for i_iter in range(config['training']['n_training_steps']): #训练50W次
    model.train(mode=True)  #准备训练
    batch = next(training_data_iter) #每个batch都是20对图（相似和不相似），以及labels
    if config['training']['mode'] == 'pair': #两两图之间的比对
        node_features, edge_features, from_idx, to_idx, graph_idx, labels = get_graph(batch) #从图中获取数据
        labels = labels.to(device) #将属性送到设备中等待训练
    else:
        node_features, edge_features, from_idx, to_idx, graph_idx = get_graph(batch)

    #将待训练数据输入模型，然后得到预测数据，其中graph_vectors就是预测数据
    graph_vectors = model(node_features.to(device), edge_features.to(device), from_idx.to(device), to_idx.to(device),
                          graph_idx.to(device), training_n_graphs_in_batch) # 将数据放到模型中开始训练 这是 predict_value，


    if config['training']['mode'] == 'pair': #两两比对
        x, y = reshape_and_split_tensor(graph_vectors, 2)

        #计算损失
        loss = pairwise_loss(x, y, labels,
                             loss_type=config['training']['loss'],
                             margin=config['training']['margin'])

        is_pos = (labels == torch.ones(labels.shape).long().to(device)).float() # 20对数据的标签，相似或者不相似
        is_neg = 1 - is_pos
        n_pos = torch.sum(is_pos)

        n_neg = torch.sum(is_neg)

        # print("n_pos:")
        # print(n_pos)
        # print(n_neg)
        sim = compute_similarity(config, x, y)#计算两个Tensor的距离 当前使用的是欧式距离
        sim_pos = torch.sum(sim * is_pos) / (n_pos + 1e-8)
        sim_neg = torch.sum(sim * is_neg) / (n_neg + 1e-8)
    else:
        x_1, y, x_2, z = reshape_and_split_tensor(graph_vectors, 4)
        loss = triplet_loss(x_1, y, x_2, z,
                            loss_type=config['training']['loss'],
                            margin=config['training']['margin'])

        sim_pos = torch.mean(compute_similarity(config, x_1, y))
        sim_neg = torch.mean(compute_similarity(config, x_2, z))

    graph_vec_scale = torch.mean(graph_vectors ** 2)
    if config['training']['graph_vec_regularizer_weight'] > 0:
        loss = loss + (config['training']['graph_vec_regularizer_weight'] *  0.5 * graph_vec_scale) #计算损失
        # loss +=  (config['training']['graph_vec_regularizer_weight'] *  0.5 * graph_vec_scale)

    optimizer.zero_grad() #优化清零
    loss.backward(torch.ones_like(loss))  #后向传播
    # loss.backward(torch.ones_like(loss).clone())  #
    nn.utils.clip_grad_value_(model.parameters(), config['training']['clip_value'])
    optimizer.step()

    sim_diff = sim_pos - sim_neg
    accumulated_metrics['loss'].append(loss)
    accumulated_metrics['sim_pos'].append(sim_pos)
    accumulated_metrics['sim_neg'].append(sim_neg)
    accumulated_metrics['sim_diff'].append(sim_diff)


    # evaluation,验证
    if (i_iter + 1) % config['training']['print_after'] == 0: #每100次输出一次
        metrics_to_print = {
            k: torch.mean(v[0]) for k, v in accumulated_metrics.items()}
        info_str = ', '.join(
            ['%s %.4f' % (k, v) for k, v in metrics_to_print.items()])
        # reset the metrics
        accumulated_metrics = collections.defaultdict(list)

        if ((i_iter + 1) // config['training']['print_after'] % #config['training']['eval_after'] = 10， config['training']['print_after'] = 100
                config['training']['eval_after'] == 0):
            model.eval() #开始验证
            with torch.no_grad():
                accumulated_pair_auc = []
                for batch in validation_set.pairs(config['evaluation']['batch_size']):
                    node_features, edge_features, from_idx, to_idx, graph_idx, labels = get_graph(batch)
                    labels = labels.to(device)
                    eval_pairs = model(node_features.to(device), edge_features.to(device), from_idx.to(device),
                                       to_idx.to(device),
                                       graph_idx.to(device), config['evaluation']['batch_size'] * 2)

                    x, y = reshape_and_split_tensor(eval_pairs, 2)
                    similarity = compute_similarity(config, x, y)
                    pair_auc = auc(similarity, labels)
                    accumulated_pair_auc.append(pair_auc)

                accumulated_triplet_acc = []
                for batch in validation_set.triplets(config['evaluation']['batch_size']):
                    node_features, edge_features, from_idx, to_idx, graph_idx = get_graph(batch)
                    eval_triplets = model(node_features.to(device), edge_features.to(device), from_idx.to(device),
                                          to_idx.to(device),
                                          graph_idx.to(device),
                                          config['evaluation']['batch_size'] * 4)
                    x_1, y, x_2, z = reshape_and_split_tensor(eval_triplets, 4)
                    sim_1 = compute_similarity(config, x_1, y)
                    sim_2 = compute_similarity(config, x_2, z)
                    triplet_acc = torch.mean((sim_1 > sim_2).float())
                    accumulated_triplet_acc.append(triplet_acc.cpu().numpy())

                eval_metrics = {
                    'pair_auc': np.mean(accumulated_pair_auc),
                    'triplet_acc': np.mean(accumulated_triplet_acc)}
                info_str += ', ' + ', '.join(
                    ['%s %.4f' % ('val/' + k, v) for k, v in eval_metrics.items()])
            model.train()
        print('iter %d, %s, time %.2fs' % (
            i_iter + 1, info_str, time.time() - t_start))
        t_start = time.time()


        '''
        #保存模型
        # Save the model
        torch.save({'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': loss,
               }, 'models/pytorch_' + str(datetime_now)+'/conv_net_model_'+ str(epoch)+'_'+str(np.mean(accs))+'.ckpt')

        
        
        #加载并运行模型
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
