# -*- coding: utf-8 -*-
# @Time : 2021/12/8 0008 16:45
# @Author : Bobby_Liukeling
# @File : pdb_del_H.py

from rdkit.Chem import AllChem
from rdkit import Chem
import os

def del_H(filename): #对文件批量去氢
    '''

    :param filename:待删除氢原子的pdb文件
    :return:将已删除氢原子的PDB文件进行存储
    '''

    files = os.listdir(filename)  # 得到文件夹下的所有文件名称
    save_path = filename+"/delH_"

    for file in files:
        try:

            mol = AllChem.MolFromPDBFile(file)
            # mol = AllChem.MolFromPDBBlock(file)
            mol = Chem.RemoveAllHs(mol)
            Chem.MolToPDBFile(mol,save_path+file)
        except:
            print(file)


pwd = os.path.dirname(os.path.realpath(__file__)) #当前文件夹下

filename = pwd+r'/xyz_changeto_pdb/xyz/pdb'
mol = del_H(filename)



'dsgdb9nsd_000008.pdb'



