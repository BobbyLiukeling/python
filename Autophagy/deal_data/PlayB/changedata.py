# -*- coding: utf-8 -*-
# @Time : 2021/7/9 0009 9:43
# @Author : Bobby_Liukeling
# @File : changedata.py
import pandas as pd
import pdb

old_data = pd.read_excel("../自噬数据库内容.xlsx")
updata = pd.read_excel("updata.xlsx")
# temp = pd.read_excel('../autophagy-GO-treat1.xls')

# a = old_data['Uniprot Acc'].tolist()
# b = temp['Acc(id)'].tolist()
# pdb.set_trace()
# pd.concat([df1, df3], sort=False)




Add_AccId = updata[updata["add_AccId"] == True] #新增AccId
old_AccId = updata[updata["add_AccId"] == False]
# pdb.set_trace()
old_AccId = old_AccId[['AccId','add_pro_type','remark']]
old_AccId.rename(columns={'AccId':'Uniprot Acc','add_pro_type':'Add_PROTEIN'},inplace=True)

for index,rows in old_AccId.iterrows():
    if pd.isnull(rows['remark']):
        pass
    else:
        # pdb.set_trace()
        temp_str = rows['remark']+" 在最新的查询结果中未查到该条数据 "
        old_AccId.remark[old_AccId.remark == rows['remark']] = temp_str #修改remark
        # old_AccId[old_AccId['Uniprot Acc'] == rows['Uniprot Acc']]['remark']

Add_AccId.rename(columns={'AccId':'Uniprot Acc','add_pro_type':'Add_PROTEIN'},inplace=True)
Add_AccId['remark'] = "新增Uniprot Acc数据"


old_data = old_data.merge(old_AccId,on = 'Uniprot Acc',how = 'left') #将更新的Pro数据加到末尾
# pdb.set_trace()

#将新增AccId数据添加到数据末尾
old_data = pd.concat([old_data,Add_AccId[['Uniprot Acc','Add_PROTEIN','remark']]],sort = False)

old_data.to_excel("last_data.xlsx")



