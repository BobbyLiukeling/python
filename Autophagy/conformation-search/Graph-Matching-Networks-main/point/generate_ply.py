# -*- coding: utf-8 -*-
# @Time : 2022/1/18 0018 17:30
# @Author : Bobby_Liukeling
# @File : generate_ply.py



# 一
# 注意vertex 和tri都是(N, 3)格式，三角形编号从1开始．
def dump_to_ply(vertex, tri, wfp):
    # index in tri should begin from 1.
    # vertex in shape (3,N ), tri in shape (3, N)
    header = """ply
    format ascii 1.0
    element vertex {}
    property float x
    property float y
    property float z
    element face {}
    property list uchar int vertex_indices
    end_header"""

    n_vertex = vertex.shape[1]
    n_face = tri.shape[1]
    header = header.format(n_vertex, n_face)

    with open(wfp, 'w') as f:
        f.write(header + '\n')
        for i in range(n_vertex):
            x, y, z = vertex[:, i]
            f.write('{:.4f} {:.4f} {:.4f}\n'.format(x, y, z))
        for i in range(n_face):
            idx1, idx2, idx3 = tri[:, i]
            f.write('3 {} {} {}\n'.format(idx1 - 1, idx2 - 1, idx3 - 1))
    print('Dump tp {}'.format(wfp))



# 二
import open3d as o3d
import numpy as np

def makePlyFile(xyzs, labels, fileName='makeply.ply'):
    '''Make a ply file for open3d.visualization.draw_geometries
    :param xyzs:    numpy array of point clouds 3D coordinate, shape (numpoints, 3).
    :param labels:  numpy array of point label, shape (numpoints, ).
    '''
    RGBS = [
        (0, 255, 255),
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (0, 0, 0),
        (255, 0, 255)
    ]

    with open(fileName, 'w') as f:
        f.write('ply\n')
        f.write('format ascii 1.0\n')
        f.write('comment PCL generated\n')
        f.write('element vertex {}\n'.format(len(xyzs)))
        f.write('property float x\n')
        f.write('property float y\n')
        f.write('property float z\n')
        f.write('property uchar red\n')
        f.write('property uchar green\n')
        f.write('property uchar blue\n')
        f.write('end_header\n')
        for i in range(len(xyzs)):
            r, g, b = RGBS[int(labels[i])-1]
            x, y, z = xyzs[i]
            f.write('{} {} {} {} {} {}\n'.format(x, y, z, r, g, b))

if __name__ == "__main__":
    numpoints = 2000  # 2000个点
    xyzs = np.random.rand(numpoints, 3)
    labels = np.random.randint(0, 4, numpoints)  # 4种label
    makePlyFile(xyzs, labels, 'demo.ply')
    pcd = o3d.io.read_point_cloud('demo.ply')
    o3d.visualization.draw_geometries([pcd])



# 三 有面和nx ny···
import open3d as o3d
import trimesh
import numpy as np

pcd = o3d.io.read_point_cloud("pointcloud.ply")
pcd.estimate_normals()

# estimate radius for rolling ball
distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 1.5 * avg_dist

mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
           pcd,
           o3d.utility.DoubleVector([radius, radius * 2]))

# create the triangular mesh with the vertices and faces from open3d
tri_mesh = trimesh.Trimesh(np.asarray(mesh.vertices), np.asarray(mesh.triangles),
                          vertex_normals=np.asarray(mesh.vertex_normals))

trimesh.convex.is_convex(tri_mesh)



# 四
import numpy as np
# Function to create point cloud file
def create_output(vertices, colors, filename):
    colors = colors.reshape(-1, 3)
    vertices = np.hstack([vertices.reshape(-1, 3), colors])
    np.savetxt(filename, vertices, fmt='%f %f %f %d %d %d')     # 必须先写入，然后利用write()在头部插入ply header
    ply_header = '''ply
    		format ascii 1.0
    		element vertex %(vert_num)d
    		property float x
    		property float y
    		property float z
    		property uchar red
    		property uchar green
    		property uchar blue
    		end_header
    		\n
    		'''
    with open(filename, 'r+') as f:
        old = f.read()
        f.seek(0)
        f.write(ply_header % dict(vert_num=len(vertices)))
        f.write(old)


if __name__ == '__main__':
    # Define name for output file
    output_file = 'Andre_Agassi_0015.ply'
    a = np.load("Andre_Agassi_0015.npy")
    b = np.float32(a)
#   43867是我的点云的数量，用的时候记得改成自己的
    one = np.ones((43867,3))
    one = np.float32(one)*255
#    points_3D = np.array([[1,2,3],[3,4,5]]) # 得到的3D点（x，y，z），即2个空间点
#    colors = np.array([[0, 255, 255], [0, 255, 255]])   #给每个点添加rgb
    # Generate point cloud
    print("\n Creating the output file... \n")
#    create_output(points_3D, colors, output_file)
    create_output(b, one, output_file)
