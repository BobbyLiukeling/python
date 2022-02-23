# -*- encoding: utf-8 -*-
# @author : bobby
# @time : 2020/1/20 12:03

import pandas as pd
import pdb


df = pd.read_csv("HR.csv")
#得到标注
pdb.set_trace()
label = df['left']
df = df.drop('left',axis=1)#以列删除，默认为行
#2、数据清洗
df = df.dropna(subset=['satisfaction_levle','last_evaluation'])
df = df[df['satisfaction_level']<=1]

