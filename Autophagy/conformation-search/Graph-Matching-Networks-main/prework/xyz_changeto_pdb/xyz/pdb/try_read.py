# -*- coding: utf-8 -*-
# @Time : 2021/12/19 0019 20:14
# @Author : Bobby_Liukeling
# @File : try_read.py

from rdkit.Chem import AllChem
from rdkit import Chem
import os


def del_H(filename): #对文件批量去氢
    '''

    :param filename:待删除氢原子的pdb文件
    :return:将已删除氢原子的PDB文件进行存储
    注意一定要在当前文件夹下运行，否则会出问题，不知道为啥
    '''

    files = os.listdir(filename)  # 得到文件夹下的所有文件名称
    # father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
    # save_path = filename+"/delH_"
    save_path = filename+"delH_pdb/delH_"



    for file in files:
        if file.startswith('dsg'):
            # file = filename+file
            mol = AllChem.MolFromPDBFile(file)
            # mol = AllChem.MolFromPDBBlock(file)
            mol = Chem.RemoveAllHs(mol)
            Chem.MolToPDBFile(mol,save_path+file)
            # print("ok")



# pwd = os.path.dirname(os.path.realpath(__file__)) #当前文件夹下
# filename = pwd

filename = '/root/liukeling/autophagy/conformation-search/Graph-Matching-Networks-main/prework/xyz_changeto_pdb/all_xyz/pdb/'
mol = del_H(filename)
