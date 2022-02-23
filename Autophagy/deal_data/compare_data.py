# -*- coding: utf-8 -*-
# @Time : 2021/7/2 0002 20:15
# @Author : Bobby_Liukeling
# @File : compare_data.py

import pandas as pd
import pdb
import numpy as np

old_data = pd.read_excel("自噬数据库内容.xlsx")
old_protein_NAN = old_data[old_data[["PROTEIN"]].isnull().T.any()][['Uniprot Acc']]
old_data = old_data[['Uniprot Acc', 'PROTEIN']] #待对比的数据
old_data.rename(columns={"Uniprot Acc":"AccId",'PROTEIN':'pro_type'},inplace=True)

new_data_accomplish = pd.read_excel("Acc_data.xlsx")
new_data_accomplish = new_data_accomplish[["AccId","pro_type"]]


with open("error_list1.txt", "r") as file:  #
    data = file.read()
    pdb.set_trace()

new_data_unaccomplish = pd.read_excel("autophagy-Go-treat1.xls")
new_data_unaccomplish  = new_data_unaccomplish[["Acc(id)"]]
new_data_unaccomplish.rename(columns={"Acc(id)":"AccId"},inplace=True)#修改列名
new_data_unaccomplish["pro_type"] = np.nan


#将由pro和没Pro的数据进行拼接
new_data = pd.merge(new_data_accomplish,new_data_unaccomplish['AccId'],on=['AccId'], how='right')

#'old_pro_type'老pro数据，'add_pro_type':新增Pro数据，'add_AccId'：新增AccId'
updata = pd.DataFrame(columns=['AccId','old_pro_type','add_pro_type','add_AccId']) #比较之后整合是数据

#将新增的数据提取出来
for index, row in new_data.iterrows():
    temp = row['AccId']
    # pdb.set_trace()
    if temp in old_data['AccId'].values: #AccId 未更新

        a = old_data[old_data['AccId'] == temp]['pro_type'].values.tolist()[0] #取出数据,旧的pro
        b = row['pro_type'] #新的pro

        if pd.isnull(a):#原数据为空
            if pd.isnull(b): #两者均无数据
                updata = updata.append([row['AccId'], np.nan, np.nan, False], ignore_index=True)
            else:
                updata = updata.append([row['AccId'], np.nan, b, False], ignore_index=True)

        else:#原数据不为空
            if pd.isnull(b):#新数据为空
                print("data is error1")
                pdb.set_trace()

            else:
                a = set(a.split(","))
                b = set(b.split(","))

                if a<b: #pro数据已经更新
                    updata_pro = list(b-a)
                    updata = updata.append([row['AccId'], ",".join(a), ",".join(updata_pro), False], ignore_index=True)

                elif a == b: #未更新数据
                    updata = updata.append([row['AccId'], ",".join(a), np.nan, False], ignore_index=True)

                else: #新数据比就数据少
                    print("data is error2")
                    pdb.set_trace()


    else : #AccId 有更新,直接追加数据
        if len(row['pro_type'])>0: #pro数据不为空
            updata = updata.append([row['AccId'],np.nan,row['pro_type'],True],ignore_index=True)
        else: #Pro数据为空
            updata = updata.append([row['AccId'], np.nan, np.nan, True], ignore_index=True)

print(updata.head())
updata.to_excel("updata.xlsx")



