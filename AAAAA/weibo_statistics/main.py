# -*- encoding: utf-8 -*-
# @author : bobby
# @time : 2020/2/12 21:55
import pandas as pd
import pdb
df = pd.read_csv('my_dict.csv')

# count = len(df['sentiment_score'] = 1)

s = df['sentiment_score']
# print(s)
count = 0
a = 0
for i in s:
    if i==1:
        count = count+1
    elif i==0:
        a = a+1
pdb.set_trace()