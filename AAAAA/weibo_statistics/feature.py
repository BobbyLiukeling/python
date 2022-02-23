# -*- encoding: utf-8 -*-
# @author : bobby
# @time : 2020/2/13 11:16
'''
readme
将情感得分用直方图显示出来
用以分析在个得分段中，情感得分的分布情况
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pdb
sentiments_totle = 'my_dict.csv'
data = pd.read_csv(sentiments_totle)

#列索引
bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
labels = ['[0,0.1)', '[0.1,0.2)', '[0.2,0.3)', '[0.3,0.4)',
          '[0.4,0.5)', '[0.5,0.6)', '[0.6,0.7)', '[0.7,0.8)', '[0.8,0.9)', '[0.9,1)']

data['sentiment_score_layer'] = pd.cut(data.sentiment_score,bins,labels = labels)
aggR = data.groupby(by = ['sentiment_score_layer'])['sentiment_score'].agg({'sentiment_score':np.size})
pAgg = round(aggR/aggR.sum(),2,)

#绘图
plt.figure(figsize=(10,6)) #设置画布长、宽
pAgg['sentiment_score'].plot(kind = 'bar',width = 0.6, fontsize = 16)
plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文标签
plt.title('情感得分分布直方图', fontsize = 20)
plt.ylabel('得分百分比') #y轴标题
plt.show()
plt.savefig('sentiment_histogram')
