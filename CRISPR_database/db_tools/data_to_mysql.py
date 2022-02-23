#!/usr/bin/env python
# encoding: utf-8
'''
@author: bobby
@file: data_to_mysql.py
@time: 7/22/20 12:05 AM
'''


import pymysql
import numpy as py
import pandas as pd
import pdb
import sqlalchemy as sqla

class Insert_to_Mysql:
    # def __init__(self):
    #
    #
    #     self.db = pymysql.connect( #连接数据库
    #         host = '127.0.0.1',
    #         port = 3306,
    #         user = 'bobby',
    #         password = '520lkl',
    #         db = 'CRISPR',
    #         charset = 'utf8',
    #     )
    #
    #     self.cursor = self.db.cursor() #创建一个游标对象

    def xsl_to_csv(self):
        '''
        读入数据并将数据规范化
        :return:
        '''
        df = pd.read_excel('CRISPR.xlsx')
        df.rename(columns={
            'Abrevation (3 let)':'CRISPR_name','Clade':'CRISPR_type','Length':'CRISPR_Length','PAM (consensus)':'PAM_Consensus',
            'Cas9 AA sequence':'CRISPR_Consensus','PI domain sequence':'PI_Sequence',
        },inplace=True)

        df = df.dropna()
        df = df.drop_duplicates()

        df['PI_Length'] = df['PIDomain_Sequence'].str.len() #comput the length of PI_sequence
        df['PI_Length'] = df['PI_Length'].apply(lambda x: int(x))  # change the data of PI_Length type into int
        df['PAM_Length'] = df['PAM_Consensus'].str.len() #comput the length of PAM consensus
        df['CRISPR_Length'] = df['CRISPR_Length'].apply(lambda x:int(x)) #　change the data of CRISPR_length type into int
        # df['PI_Start_Position'] = df[df['PI_Start_position'].apply(lambda x:int(x))] #the start position of PAM sequence in CRISPR_senquence

        # pdb.set_trace()


        df.to_csv('CRISPR_data_latest.csv')
        df.to_excel('CRISPR_data_latest.xlsx')

        return df

    def read_csv(self):
        df = pd.read_csv('CRISPR_data.csv')
        df = df.drop(df.columns[0], axis=1,inplace=True)
        return df

    def data_into_mysql(self,df): #利用pandas中自带的mysql模块插入数据,不用新建表格，会根据数据特征自动创建表格，只需要新建数据库
        try:
            conn = sqla.create_engine('mysql+pymysql://root:867425@localhost:3306/CRISPR?charset=utf8')  #不要留空，其中CRISPR是数据库
            pd.io.sql.to_sql(df,'database_query_crispr',conn,schema='CRISPR',if_exists='replace') #其中 database_query_crispr是待插入的数据库表，只需要指定表名，不需要再数据库中新建表
        except Exception as e:
            print(e)
            pdb.set_trace()
            pass


if __name__ == "__main__":
    Main = Insert_to_Mysql()
    Main.data_into_mysql(Main.xsl_to_csv())
