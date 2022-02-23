# -*- encoding: utf-8 -*-
# @author : bobby
# @time : 2020/2/12 21:55
'''
readme
将从微博爬取到的评论的情感评分后进行前期数据的异常值分析
方法：箱线图，查看是否存在异常值
'''
import pandas as pd
import pdb
cater = 'my_dict.xlsx'
data = pd.read_excel(cater,index_col='text')
print(data.describe()) #输出读出数据的基本信息
'''
输出结果:
              score
count  21558.000000
mean       0.607482
std        0.328979
min        0.000000
25%        0.331351
50%        0.663319
75%        0.928018
max        1.000000
'''
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] #导入图像库
plt.rcParams['axes.unicode_minus'] = False #避免中文显示乱码
plt.figure()#正常显示负号
p = data.boxplot(return_type='dict')

x = p['fliers'][0].get_xdata() # 'flies'即为异常值的标签
y = p['fliers'][0].get_ydata()
y.sort() #从小到大排序，该方法直接改变原对象

#用annotate添加注释
#其中有些相近的点，注解会出现重叠，难以看清，需要一些技巧来控制。
#以下参数都是经过调试的，需要具体问题具体调试。
for i in range(len(x)):
  if i>0:
    plt.annotate(y[i], xy = (x[i],y[i]), xytext=(x[i]+0.05 -0.8/(y[i]-y[i-1]),y[i]))
  else:
    plt.annotate(y[i], xy = (x[i],y[i]), xytext=(x[i]+0.08,y[i]))
plt.show() #展示箱线图



