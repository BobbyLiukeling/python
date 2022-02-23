# -*- coding: utf-8 -*-
# @Time : 2022/1/19 0019 11:01
# @Author : Bobby_Liukeling
# @File : try3.py


import copy,pdb
import numpy as np
import open3d as o3
from probreg import cpd
# path1 = 'auto_sdf/1N1.ply'
path2 = 'auto_sdf/1N1_2.ply'

path1 = 'auto_sdf/4B7_2_normal.ply'
# path2 = 'auto_sdf/4B7_normal.ply'

# path1 = 'auto_sdf/1N1_normal.ply'
# path2 = 'auto_sdf/1N1_2_normal.ply'

# path1 = 'colored/pred_Chair_0.ply'
# path2 = 'colored/pred_Mug_0.ply'

# path1 = 'colored/pred_Mug_1.ply'
# path2 = 'colored/pred_Mug_0.ply'

# load source and target point cloud
source = o3.io.read_point_cloud(path1)
target = o3.io.read_point_cloud(path2)
# target = copy.deepcopy(source)
# transform target point cloud
th = np.deg2rad(30.0)
target.transform(np.array([[np.cos(th), -np.sin(th), 0.0, 0.0],
                           [np.sin(th), np.cos(th), 0.0, 0.0],
                           [0.0, 0.0, 1.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]]))
# source = source.voxel_down_sample(voxel_size=0.005)
# target = target.voxel_down_sample(voxel_size=0.005)

# compute cpd registration
tf_param, a, b = cpd.registration_cpd(source, target) # a,b,有可能是fitness，rmsd
A = cpd.registration_cpd(source, target) # a,b,有可能是fitness，rmsd

print(a," ",b)

result = copy.deepcopy(source)
result.points = tf_param.transform(result.points)

# pdb.set_trace()
# draw result
source.paint_uniform_color([1, 0, 0])
target.paint_uniform_color([0, 1, 0])
result.paint_uniform_color([0, 0, 1])
# o3.visualization.draw_geometries([source, target, result])
# o3.visualization.draw_geometries([target, source])
o3.visualization.draw_geometries([target, result])


#compute rmse !

# source = result
# from scipy.spatial import cKDTree
# from probreg import math_utils as mu
# target_tree = cKDTree(np.asarray(target.points), leafsize=10)
# rmse = mu.compute_rmse(np.asarray(source.points),target_tree)

# print(rmse)

