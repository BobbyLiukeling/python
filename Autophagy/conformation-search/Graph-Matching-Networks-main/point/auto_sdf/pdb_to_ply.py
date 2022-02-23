# -*- coding: utf-8 -*-
# @Time : 2022/1/18 0018 17:56
# @Author : Bobby_Liukeling
# @File : sdf_to_ply.py






import torch
# from torch_geometric.data import Data
from rdkit.Chem import AllChem


import os
import numpy as np
import copy,pdb

# #元素周期表对应编号
# atmos = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20,
#  'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30, 'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36, 'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40,
#  'Nb': 41, 'Mo': 42, 'Tc': 43, 'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49, 'Sn': 50, 'Sb': 51, 'Te': 52, 'I': 53, 'Xe': 54, 'Cs': 55, 'Ba': 56, 'La': 57, 'Ce': 58, 'Pr': 59, 'Nd': 60,
#  'Pm': 61, 'Sm': 62, 'Eu': 63, 'Gd': 64, 'Tb': 65, 'Dy': 66, 'Ho': 67, 'Er': 68, 'Tm': 69, 'Yb': 70, 'Lu': 71, 'Hf': 72, 'Ta': 73, 'W': 74, 'Re': 75, 'Os': 76, 'Ir': 77, 'Pt': 78, 'Au': 79, 'Hg': 80,
#  'Tl': 81, 'Pb': 82, 'Bi': 83, 'Po': 84, 'At': 85, 'Rn': 86, 'Fr': 87, 'Ra': 88, 'Ac': 89, 'Th': 90, 'Pa': 91, 'U': 92, 'Np': 93, 'Pu': 94, 'Am': 95, 'Cm': 96, 'Bk': 97, 'Cf': 98, 'Es': 99, 'Fm': 100,
#  'Md': 101, 'No': 102, 'Lr': 103, 'Rf': 104, 'Db': 105, 'Sg': 106, 'Bh': 107, 'Hs': 108, 'Mt': 109, 'Ds': 110, 'Rg': 111, 'Cn': 112, 'Nh': 113, 'Fl': 114, 'Mc': 115, 'Lv': 116, 'Ts': 117, 'Og': 118}
#
#
# #生成255个RGB
# from itertools import product
# a = [0,63,127,191,255]
# RGB_list = list(product(a, repeat=3))
#
# atom_RGB_map = {}
# for key,rgb in zip(atmos.keys(),RGB_list[:117]):
#     atom_RGB_map[key] = rgb


atom_RGB_map = {'H': (0, 0, 0), 'He': (0, 0, 63), 'Li': (0, 0, 127), 'Be': (0, 0, 191), 'B': (0, 0, 255), 'C': (0, 63, 0),
                'N': (0, 63, 63), 'O': (0, 63, 127), 'F': (0, 63, 191), 'Ne': (0, 63, 255), 'Na': (0, 127, 0), 'Mg': (0, 127, 63),
                'Al': (0, 127, 127), 'Si': (0, 127, 191), 'P': (0, 127, 255), 'S': (0, 191, 0), 'Cl': (0, 191, 63), 'Ar': (0, 191, 127),
                'K': (0, 191, 191), 'Ca': (0, 191, 255), 'Sc': (0, 255, 0), 'Ti': (0, 255, 63), 'V': (0, 255, 127), 'Cr': (0, 255, 191),
                'Mn': (0, 255, 255), 'Fe': (63, 0, 0), 'Co': (63, 0, 63), 'Ni': (63, 0, 127), 'Cu': (63, 0, 191), 'Zn': (63, 0, 255),
                'Ga': (63, 63, 0), 'Ge': (63, 63, 63), 'As': (63, 63, 127), 'Se': (63, 63, 191), 'Br': (63, 63, 255), 'Kr': (63, 127, 0),
                'Rb': (63, 127, 63), 'Sr': (63, 127, 127), 'Y': (63, 127, 191), 'Zr': (63, 127, 255), 'Nb': (63, 191, 0),
                'Mo': (63, 191, 63), 'Tc': (63, 191, 127), 'Ru': (63, 191, 191), 'Rh': (63, 191, 255), 'Pd': (63, 255, 0),
                'Ag': (63, 255, 63), 'Cd': (63, 255, 127), 'In': (63, 255, 191), 'Sn': (63, 255, 255), 'Sb': (127, 0, 0),
                'Te': (127, 0, 63), 'I': (127, 0, 127), 'Xe': (127, 0, 191), 'Cs': (127, 0, 255), 'Ba': (127, 63, 0), 'La': (127, 63, 63),
                'Ce': (127, 63, 127), 'Pr': (127, 63, 191), 'Nd': (127, 63, 255), 'Pm': (127, 127, 0), 'Sm': (127, 127, 63),
                'Eu': (127, 127, 127), 'Gd': (127, 127, 191), 'Tb': (127, 127, 255), 'Dy': (127, 191, 0), 'Ho': (127, 191, 63),
                'Er': (127, 191, 127), 'Tm': (127, 191, 191), 'Yb': (127, 191, 255), 'Lu': (127, 255, 0), 'Hf': (127, 255, 63),
                'Ta': (127, 255, 127), 'W': (127, 255, 191), 'Re': (127, 255, 255), 'Os': (191, 0, 0), 'Ir': (191, 0, 63), 'Pt': (191, 0, 127),
                'Au': (191, 0, 191), 'Hg': (191, 0, 255), 'Tl': (191, 63, 0), 'Pb': (191, 63, 63), 'Bi': (191, 63, 127), 'Po': (191, 63, 191),
                'At': (191, 63, 255), 'Rn': (191, 127, 0), 'Fr': (191, 127, 63), 'Ra': (191, 127, 127), 'Ac': (191, 127, 191),
                'Th': (191, 127, 255), 'Pa': (191, 191, 0), 'U': (191, 191, 63), 'Np': (191, 191, 127), 'Pu': (191, 191, 191),
                'Am': (191, 191, 255), 'Cm': (191, 255, 0), 'Bk': (191, 255, 63), 'Cf': (191, 255, 127), 'Es': (191, 255, 191),
                'Fm': (191, 255, 255), 'Md': (255, 0, 0), 'No': (255, 0, 63), 'Lr': (255, 0, 127), 'Rf': (255, 0, 191),
                'Db': (255, 0, 255), 'Sg': (255, 63, 0), 'Bh': (255, 63, 63), 'Hs': (255, 63, 127), 'Mt': (255, 63, 191),
                'Ds': (255, 63, 255), 'Rg': (255, 127, 0), 'Cn': (255, 127, 63), 'Nh': (255, 127, 127), 'Fl': (255, 127, 191),
                'Mc': (255, 127, 255), 'Lv': (255, 191, 0), 'Ts': (255, 191, 63)}


def create_ply(pdb_path):
    mol = AllChem.MolFromPDBFile(pdb_path)
    atom_num = mol.GetNumAtoms()  # 原子总数
    ply_header = '''ply
format ascii 1.0
element vertex {} 
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''.format(atom_num)

    # 获取原子顶点属性
    f = open(pdb_path.split('.')[0]+'_normal.ply','w')
    f.write(ply_header)

    # 获得原子坐标
    xyz = []
    for atom in mol.GetAtoms():
        x, y, z = mol.GetConformer().GetAtomPosition(atom.GetIdx())  # 原子坐标
        xyz.append([x, y, z])
    #坐标归一化
    xyz = np.array(xyz)
    # 求质心，也就是一个平移量，实际上就是求均值


    centroid = np.mean(xyz, axis=0)
    xyz = xyz - centroid
    m = np.max(np.sqrt(np.sum(xyz ** 2, axis=1)))
    # 对点云进行缩放
    xyz = xyz / m
    xyz = xyz.round(2)
    for atom,site in zip(mol.GetAtoms(),xyz):
        RGB = atom_RGB_map[atom.GetSymbol()]  # 颜色编码
        x, y, z = site
        temp = "{} {} {} {} {} {}".format(str(x),str(y),str(z),str(RGB[0]),str(RGB[1]),str(RGB[2])+'\n') #生成一行数据
        f.write(temp)
        # pdb.set_trace()

# path = "4B7_2"
# path = "4B7"
path = "1N1"
# path = "1N1_2"
create_ply(path+'.pdb')
import open3d as o3d

pcd = o3d.io.read_point_cloud(path+'_normal.ply')
# o3d.visualization.draw_geometries([pcd])

# def pc_normalize(path):
#     """
#         对点云数据进行归一化
#         :param pc: 需要归一化的点云数据
#         :return: 归一化后的点云数据
#         """
#     path = path+'.pdb'
#     mol = AllChem.MolFromPDBFile(path)
#     xyz = []
#     for atom in mol.GetAtoms():
#         x, y, z = mol.GetConformer().GetAtomPosition(atom.GetIdx())  # 原子坐标
#         xyz.append([x, y, z] )
#     # pdb.set_trace()
#     xyz = np.array(xyz)
#     print(xyz)
#     # 求质心，也就是一个平移量，实际上就是求均值
#     centroid = np.mean(xyz, axis=0)
#     xyz = xyz - centroid
#     return xyz
#     # pdb.set_trace()
#     # m = np.max(np.sqrt(np.sum(pc ** 2, axis=1)))
#     # # 对点云进行缩放
#     # pc = pc / m
#     # return pc
#
#
# pc_normalize(path)
