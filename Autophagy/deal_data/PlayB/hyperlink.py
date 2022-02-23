# -*- coding: utf-8 -*-
# @Time : 2021/7/16 0016 16:55
# @Author : Bobby_Liukeling
# @File : hyperlink.py
import pandas as pd
import pdb

df = pd.read_excel("last_data.xlsx")
# df = df['Add_PROTEIN']

link = []

for index,rows in df.iterrows():

    if pd.isnull(rows['Add_PROTEIN']):
        pass
    else:
        temp = rows['Add_PROTEIN'].split(',')
        # pdb.set_trace()
        link = link+temp
links = []
for i in link:
    links.append('https://www.rcsb.org/structure/{}'.format(i))




data = pd.DataFrame(links,columns=['link'])
data.to_excel("links.xlsx")
pdb.set_trace()



