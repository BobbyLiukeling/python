# -*- coding: utf-8 -*-
# @Time : 2022/1/16 0016 18:31
# @Author : Bobby_Liukeling
# @File : try2.py


'''
Author: dongcidaci
Date: 2021-09-13 15:49:49
LastEditTime: 2021-09-13 16:03:58
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \open3d_code\test_data\02_2_caisepeizhun.py
'''
import open3d as o3d
import numpy as np
import copy,pdb


# 彩色点云配准
# 演示了一种同时使用几何和颜色进行配准的ICP变体
# 实现了颜色信息锁定与切平面的对齐

# 可视化函数
# 为了掩饰不同颜色点云之间的对齐,draw_registration_result_original_color使用原本的颜色可视化源点云.
def draw_registration_result_original_color(source, target, transformation):
    source_temp = copy.deepcopy(source)
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target])


# 输入
# 从两个文件中读取源点云和目标点云.使用单位阵作为初始化的配准矩阵.
path1 = 'auto_sdf/1N1_normal.ply'
path2 = 'auto_sdf/1N1_2_normal.ply'
# path1 = 'auto_sdf/1N1.ply'
# path2 = 'auto_sdf/1N1_2.ply'

# path1 = 'colored/pred_Chair_0.ply'
# path2 = 'colored/pred_Mug_0.ply'

# path1 = "colored/frag_115.ply"
# path2 = "colored/frag_116.ply"


print("1. Load two point clouds and show initial pose")
source = o3d.io.read_point_cloud(path1)
target = o3d.io.read_point_cloud(path2)
# draw initial alignment
current_transformation = np.identity(4)
# draw_registration_result_original_color(source, target, current_transformation)
# pdb.set_trace()
# Point-to-plane ICP
# 下面的可视化结果展示了未对其的绿色三角形纹理.这是因为几何约束不能够阻止两个平面滑动.

#point to plane ICP
current_transformation = np.identity(4)
print("2. Point-to-plane ICP registration is applied on original point")
print("   clouds to refine the alignment. Distance threshold 0.02.")

def ICP(source,target,radius):

# radius = 0.04
    source.estimate_normals(
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))
    target.estimate_normals(
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))

    result_icp = o3d.pipelines.registration.registration_icp(
        source, target, 0.02, current_transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    # print("result_icp:   ",result_icp)
    print("radius:",radius)
    print(result_icp.transformation)
    draw_registration_result_original_color(source, target, result_icp.transformation) #画出原始图

# radius = [4,2,1,0.5,0.2,0.1]
radius = [1,0.5,0.2]
for i in radius:
    ICP(source,target,i)

# colored pointcloud registration
# This is implementation of following paper
# J. Park, Q.-Y. Zhou, V. Koltun,
# Colored Point Cloud Registration Revisited, ICCV 2017

voxel_radius = [0.04, 0.02, 0.01]
max_iter = [50, 30, 14]
current_transformation = np.identity(4)
print("3. Colored point cloud registration 彩色点云配准")
for scale in range(3):
    iter = max_iter[scale]
    radius = voxel_radius[scale]
    print([iter, radius, scale])

    print("3-1. Downsample with a voxel size %.2f 下采样的点云的体素大小" % radius)
    # source_down = source.voxel_down_sample(radius)
    # target_down = target.voxel_down_sample(radius)
    source_down = source
    target_down = target

    print("3-2. Estimate normal. 法向量估计") #nx,ny,nz 有在计算法向量，所以源文件中可以不用计算法向量
    source_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))
    target_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))

    print("3-3. Applying colored point cloud registration 应用彩色点云配准")
    result_icp = o3d.pipelines.registration.registration_colored_icp(
        source_down, target_down, radius, current_transformation,
        o3d.pipelines.registration.TransformationEstimationForColoredICP(),
        o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness=1e-6,relative_rmse=1e-6,max_iteration=iter))
    current_transformation = result_icp.transformation
    print("result_icp_colored:",result_icp)
draw_registration_result_original_color(source, target, result_icp.transformation)
