# -*- coding: utf-8 -*-
# @Time : 2021/12/8 0008 15:04
# @Author : Bobby_Liukeling
# @File : torsion.py

import numpy as np
import math,pdb

from rdkit import Chem
from rdkit.Chem import AllChem



def torsion_angle(p0,p1,p2,p3):
    """
    计算四个点坐标的np.array类型数组
    二面角为（p0,p1,p2）所在平面与（p1,p2,p3）所在平面
    最终获得p[0]的二面角
    """
    b0 = -1.0*(p1 - p0)
    b1 = p2 - p1
    b2 = p3 - p2

    # normalize b1 so that it does not influence magnitude of vector
    # rejections that come next
    b1 /= np.linalg.norm(b1)

    # vector rejections
    # v = projection of b0 onto plane perpendicular to b1
    #   = b0 minus component that aligns with b1
    # w = projection of b2 onto plane perpendicular to b1
    #   = b2 minus component that aligns with b1
    v = b0 - np.dot(b0, b1)*b1
    w = b2 - np.dot(b2, b1)*b1

    # angle between v and w in a plane is the torsion angle
    # v and w may not be normalized but that's fine since tan is y/x
    x = np.dot(v, w)
    y = np.dot(np.cross(b1, v), w)
    return np.degrees(np.arctan2(y, x))


def read_coordinates_pdb(filename):
    """
    传入pdb类型文件，获得所有原子的坐标
    Read coordinates
    :param filename: Conformation，
    :param atom1: Atom 1
    :param atom2: Atom 2
    :param atom3: Atom 3
    :param atom4: Atom 4
    :return: Coordinates array
    """
    mol = Chem.MolFromPDBFile(filename)
    mol_num = mol.GetNumAtoms()#获得原子个数
    coordinates = []
    for i in range(mol_num):
        x, y, z = mol.GetConformer().GetAtomPosition(i) #获得第二个原子坐标
        coordinates.append([x, y, z])
    return np.array(coordinates, dtype=float)




#计算单个旋转角
def calc_torsion_angle(coordinates):
    """
    Calculate single torsion angle
    :param coordinates: Multidimensional array of coordinates
    :return: Torsion angle
    """
    """
    a, b, c, d are the points that make up a torsion angle.
    """
    a = coordinates[0]
    b = coordinates[1]
    c = coordinates[2]
    d = coordinates[3]
    vector_1, vector_2, vector_3 = b - a, c - b, d - c
    norm_vector_1 = np.cross(vector_1, vector_2)   # a,b,c所在平面法向量
    norm_vector_2 = np.cross(vector_2, vector_3)   # b,c,d所在平面法向量
    norm_vector_1x2 = np.cross(norm_vector_1, norm_vector_2)
    x = np.dot(norm_vector_1, norm_vector_2)
    y = np.dot(norm_vector_1x2, vector_2) / np.linalg.norm(vector_2)
    radian = np.arctan2(y, x)
    angle = radian * 180 / math.pi
    return angle


#计算全部的旋转角
def calc_angle_list(atom1, atom2, atom3, atom4):
    """
    Calculate all torsion angle
    :param atom1: Atom 1
    :param atom2: Atom 2
    :param atom3: Atom 3
    :param atom4: Atom 4
    :return: All torsion angle
    """
    angle_list = []
    for i in range(1):
    	# 文件路径
        filename = r'dsgdb9nsd_000002.xyz'
        # filename = r'dsgdb9nsd_000024.xyz'
        coordinates_arr = read_coordinates_XYZ(filename, atom1, atom2, atom3, atom4)
        print("coordinates_arr:",coordinates_arr)
        torsion_angle = calc_torsion_angle(coordinates_arr)
        print("torsion_angle:",torsion_angle)
        angle_list.append(torsion_angle)
    return angle_list

#Drawing torsion angle distribution histogram画图函数
def drawing_histogram(atom1, atom2, atom3, atom4, i):
    """
    Drawing histogram
    :param atom1: Atom 1
    :param atom2: Atom 2
    :param atom3: Atom 3
    :param atom4: Atom 4
    :param i: Angle name
    :return: None
    """
    data = calc_angle_list(atom1, atom2, atom3, atom4)

    # print(data)
    # plt.hist(data, bins=range(-180, 185, 5), edgecolor='black', linewidth=1)
    # plt.title('Torsion Angle {} Statistics Graph'.format(i))
    # plt.xlabel('Torsion Angle')
    # plt.ylabel('Frequency')
    # plt.savefig('1_{}.png'.format(i))
    # plt.show()


#主函数
def main():
    """
    Main function
    :return: None
    """
    # 需要计算的二面角，值计算这几种类型的二面角
    multi_list = [['C_0j', 'O_0i', 'C_09', 'C_07'], ['N_0k', 'C_0j', 'O_0i', 'C_09'], ['C_0s', 'N_0r', 'C_0l', 'N_0k'],
                  ['C_0t', 'C_0s', 'N_0r', 'C_0l'], ['S_13', 'C_12', 'C_0v', 'C_0u'], ['O_14', 'S_13', 'C_12', 'C_0v'],
                  ['C_1a', 'N_18', 'S_13', 'C_12'], ['C_1b', 'C_1a', 'N_18', 'S_13'], ['N_1f', 'C_1b', 'C_1a', 'N_18'],
                  ['C_1g', 'N_1f', 'C_1b', 'C_1a']]
    for i in range(10):
        atom1, atom2, atom3, atom4 = multi_list[i][0], multi_list[i][1], multi_list[i][2], multi_list[i][3]
        drawing_histogram(atom1, atom2, atom3, atom4, i)


if __name__ == '__main__':
    read_coordinates_pdb("del_h.pdb")