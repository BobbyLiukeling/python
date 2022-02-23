# -*- coding: utf-8 -*-
# @Time : 2020/10/28 0028 10:05
# @Author : Bobby_Liukeling
# @File : data_change.py
import pandas as pd
import pdb
import re


path = 'Cas9_PI真.txt'
with open(path, "r") as f:  # 打开文件
    data = f.readlines()  # 读取文件

data = pd.DataFrame(data)
data.rename(columns = {0:'key'},inplace= True)
text = re.compile(r".*[0-9]$")
data['match'] = data['key'].apply(lambda x : 1 if text.match(x.strip()) else 0)
data = data[data['match'] == 1]

#'Lpn   1215\n' 取出数据
data['Abrevation (3 let)'] = data['key'].apply(lambda x : x.split(' ')[0]) #CRISPR name
data['PI_Start_position'] = data['key'].apply(lambda x: x.split(' ')[-1][:-1]) #PIdomain 其起始位置


data1 = pd.read_csv('Cas9氨基酸序列1_真实.csv')
data.drop(columns=['match','key'],inplace = True) #删除多余的行
# data1.rename({'No':'index'},inplace=True,axis=1) #改变索引名
data = pd.merge(data1,data,how='inner') #取二者并集
data.rename(columns={'Cas9 AA sequence':'Cas9_Sequence', 'PI domain sequence':'PIDomain_Sequence'},inplace=True)
data.drop(columns = ['No'],inplace = True)


def fun(Cas9,pi_start_position):
    return Cas9[int(pi_start_position)-1:]
data['PIDomain_Sequence'] = data.apply(lambda x : fun(x['Cas9_Sequence'],x['PI_Start_position']),axis = 1)


# pdb.set_trace()

#将数据存储下来
data.to_csv('CRISPR.csv',index= False) #不要默认标签
data.to_excel('CRISPR.xlsx',index=False)






