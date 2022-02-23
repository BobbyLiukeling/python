# -*- coding: utf-8 -*-
# @Time : 2022/1/22 0022 22:15
# @Author : Bobby_Liukeling
# @File : PDB_download.py

import requests,pdb
import pandas as pd
import numpy as np
from selenium import webdriver
import time


def download_pdbfile(pdb_list):
    '''
    :param pdb_list: pdb 文件名列表
    :return: None
    '''
    count = 0
    web = webdriver.Chrome("E:/software/Python3.7.6/chromedriver.exe")
    for i in pdb_list:
        url = "https://files.rcsb.org/download/{}.pdb".format(i)
        web.get(url)

        time.sleep(1)
        count = count+1
        if count%50 == 0:
            print("this is count:",count)

def get_PDB_ID():
    data = pd.read_excel('last_data.xlsx')
    pdb_name = []
    columns_list = ['INHIBIT', 'INHIBIT', 'ALLO', 'PROTEIN', 'Add_PROTEIN']
    for column in columns_list:
        temp = data[column]
        for i in temp:
            try:
                if np.isnan(i):
                    pass
            except:
                pdb_name.extend(i.split(','))
    pdb_name = list(set(pdb_name))
    return pdb_name


if __name__ == '__main__':
    download_pdbfile(get_PDB_ID())
