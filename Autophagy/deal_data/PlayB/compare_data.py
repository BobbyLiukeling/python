# -*- coding: utf-8 -*-
# @Time : 2021/7/2 0002 20:15
# @Author : Bobby_Liukeling
# @File : compare_data.py

import pandas as pd
import pdb
import numpy as np

old_data = pd.read_excel("../自噬数据库内容.xlsx")
old_protein_NAN = old_data[old_data[["PROTEIN"]].isnull().T.any()][['Uniprot Acc']]
old_data = old_data[['Uniprot Acc', 'PROTEIN']] #待对比的数据
old_data.rename(columns={"Uniprot Acc":"AccId",'PROTEIN':'pro_type'},inplace=True)



new_data = pd.read_excel("Acc_data.xlsx")
new_data = new_data[["AccId","pro_type"]]


with open("miss_data.txt", "r") as file:  #
    data = file.read()
    file.close()

data = data.split(',')
data = pd.DataFrame(data,columns=['AccId'])
data['pro_type'] = np.nan

new_data = new_data.append(data,ignore_index=True)
# new_data = new_data.append([[data,np.nan]],ignore_index=True)


#'old_pro_type'老pro数据，'add_pro_type':新增Pro数据，'add_AccId'：新增AccId',remark 是old_data中被删除掉的数据
updata = pd.DataFrame(columns=['AccId','old_pro_type','add_pro_type','add_AccId','remark']) #比较之后整合是数据

#将新增的数据提取出来
for index, row in new_data.iterrows():
    temp = row['AccId']

    if temp in old_data['AccId'].values: #AccId 未更新

        old = old_data[old_data['AccId'] == temp]['pro_type'].values.tolist()[0] #取出数据,旧的pro
        new = row['pro_type'] #新的pro

        if pd.isnull(old):#原数据为空
            if pd.isnull(new): #两者均无数据

                updata = updata.append({'AccId': row['AccId'], 'old_pro_type': np.nan, 'add_pro_type': np.nan, 'add_AccId': False, 'remark': np.nan}, ignore_index = True)
            else:#原数据为空，新数据不为空

                updata = updata.append({'AccId': row['AccId'], 'old_pro_type': np.nan, 'add_pro_type': new, 'add_AccId': False,'remark': np.nan}, ignore_index = True)

        else:#原数据不为空
            if pd.isnull(new):#新数据为空
                print("data is error1")
                pdb.set_trace()

            else:
                #对老数据进行预处理，老数据不规范
                old = old.split(',')
                for i in old:
                    if len(i)<4:
                        old.remove(i)
                old = set(old)


                # old = set(old.split(","))
                new = set(new.split(","))

                if old<new: #
                    updata_pro = new-old
                    # pdb.set_trace()
                    updata = updata.append({'AccId':row['AccId'],'old_pro_type':",".join(old),'add_pro_type':",".join(updata_pro),'add_AccId':False,'remark':np.nan},ignore_index=True)



                elif old == new: #未更新数

                    updata = updata.append({'AccId': row['AccId'], 'old_pro_type': ",".join(old), 'add_pro_type': np.nan, 'add_AccId': False,'remark': np.nan}, ignore_index = True)

                elif old>new: #新数据比旧数据少,c
                    print("data is error2")
                    pdb.set_trace()

                else: #新数据有对旧数据进行删除
                    del_data = old - new
                    updata_pro = new-old

                    updata = updata.append({'AccId': row['AccId'], 'old_pro_type': ",".join(old-del_data), 'add_pro_type': ",".join(updata_pro), 'add_AccId': False,
                     'remark': ",".join(del_data)}, ignore_index = True)




    else : #AccId 有更新,直接追加数据
        # pdb.set_trace()

        if pd.isnull(row['pro_type']): #pro数据不为空
            updata = updata.append({'AccId': row['AccId'], 'old_pro_type': np.nan, 'add_pro_type': np.nan,
             'add_AccId': True,'remark': np.nan}, ignore_index = True)
        else: #Pro数据为空
            updata = updata.append({'AccId': row['AccId'], 'old_pro_type': np.nan, 'add_pro_type': row['pro_type'],
             'add_AccId': True,'remark': np.nan}, ignore_index = True)



print(updata.shape)
updata.to_excel("updata.xlsx")




