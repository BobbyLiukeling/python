# -*- coding: utf-8 -*-
# @Time : 2022/1/18 0018 19:02
# @Author : Bobby_Liukeling
# @File : normal.py

# @Description: <Open3D估计法向量，可视化，存储为文件>

import open3d as o3d
import os

path = os.path.abspath(os.path.join(os.getcwd(), "../"))
path = path + "/pcds/bunny.pcd"
normalPath = path.replace(".pcd", "_normal.pcd")
print(path)
print(normalPath)

print("Load a pcd point cloud, print it, and render it")
pcd = o3d.io.read_point_cloud(path)
pcd.paint_uniform_color([0.5, 0.5, 0.5])  # 把所有点渲染为灰色（灰兔子）
print(pcd)  # 输出点云点的个数
# print(o3d.np.asarray(pcd.points))  # 输出点的三维坐标
o3d.visualization.draw_geometries([pcd], "Open3D origin points", width=800, height=600, left=50, top=50,
                                  point_show_normal=False, mesh_show_wireframe=False,
                                  mesh_show_back_face=False)

print("Downsample the point cloud with a voxel of 0.002")
downpcd = pcd.voxel_down_sample(voxel_size=0.002)  # 下采样滤波，体素边长为0.002m
print(downpcd)
o3d.visualization.draw_geometries([downpcd], "Open3D downsample points", width=800, height=600, left=50, top=50,
                                  point_show_normal=False, mesh_show_wireframe=False,
                                  mesh_show_back_face=False)

print("Recompute the normal of the downsampled point cloud")
# 混合搜索  KNN搜索  半径搜索
# downpcd.estimate_normals(
#     search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=20))  # 计算法线，搜索半径1cm，只考虑邻域内的20个点
downpcd.estimate_normals(
    search_param=o3d.geometry.KDTreeSearchParamKNN(knn=20))  # 计算法线，只考虑邻域内的20个点
# downpcd.estimate_normals(
#     search_param=o3d.geometry.KDTreeSearchParamRadius(radius=0.01))  # 计算法线，搜索半径1cm，只考虑邻域内的20个点

o3d.visualization.draw_geometries([downpcd], "Open3D normal estimation", width=800, height=600, left=50, top=50,
                                  point_show_normal=True, mesh_show_wireframe=False,
                                  mesh_show_back_face=False)  # 可视化法线
print("Print a normal vector of the 0th point")
print(downpcd.normals[0])  # 输出0点的法向量值

print("Print the normal vectors of the first 10 points")
print(o3d.np.asarray(downpcd.normals)[:10, :])  # 输出前10个点的法向量

# std::vector<Eigen::Vector3d> with 381 elements. 转换为nparry 以打印访问
# normals = o3d.np.asarray(downpcd.normals)
# print(normals)

# 可视化法向量的点，并存储法向量点到文件
normal_point = o3d.utility.Vector3dVector(downpcd.normals)
normals = o3d.geometry.PointCloud()
normals.points = normal_point
normals.paint_uniform_color((0, 1, 0))  # 点云法向量的点都以绿色显示
o3d.visualization.draw_geometries([pcd, normals], "Open3D noramls points", width=800, height=600, left=50, top=50,
                                  point_show_normal=False, mesh_show_wireframe=False,
                                  mesh_show_back_face=False)
o3d.io.write_point_cloud(normalPath, normals)
