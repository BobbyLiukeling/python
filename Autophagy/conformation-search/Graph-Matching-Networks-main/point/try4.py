# -*- coding: utf-8 -*-
# @Time : 2022/1/20 0020 20:51
# @Author : Bobby_Liukeling
# @File : try4.py
import open3d as o3d
import copy,pdb
import numpy as np
import open3d as o3
from probreg import cpd
# path1 = 'auto_sdf/1N1.ply'
# path2 = 'auto_sdf/1N1_2.ply'

# path1 = 'auto_sdf/4B7_2_normal.ply'
# path2 = 'auto_sdf/4B7_normal.ply'
path1 = 'auto_sdf/1N1_normal.ply'
path2 = 'auto_sdf/1N1_2_normal.ply'

# load source and target point cloud
source = o3.io.read_point_cloud(path1)
target = o3.io.read_point_cloud(path2)

th = np.deg2rad(30.0)
target.transform(np.array([[np.cos(th), -np.sin(th), 0.0, 0.0],
                           [np.sin(th), np.cos(th), 0.0, 0.0],
                           [0.0, 0.0, 1.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]]))


# compute cpd registration
tf_param, a, b = cpd.registration_cpd(source, target) # a,b,有可能是fitness，rmse
print(a," ",b)

result = copy.deepcopy(source)
result.points = tf_param.transform(result.points)
source = result
