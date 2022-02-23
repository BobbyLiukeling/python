# -*- coding: utf-8 -*-
# @Time : 2022/1/11 0011 17:58
# @Author : Bobby_Liukeling
# @File : try1.py

import networkx as nx
import gmatch4py as gm

G1 = nx.Graph()
G1.add_edge("1", "2")
G1.add_edge("1", "3")
G2 = nx.Graph()
G2.add_edge("1", "2")
G2.add_edge("3", "1")  # Changing the direction (no impact if working)
G2.add_edge("3", "4")
GM1 = gm.graph.Graph(G1)
GM2 = gm.graph.Graph(G2)

# print(type(GM1.size_edge_union(GM2) == 3))
# print(GM1.size_edge_union(GM2) == 3)

# print(GM1.edges())
ged=gm.GraphEditDistance(1,1,1,1)
ged = gm.GraphEditDistance(1,1,1,1)
ged.set_attr_graph_used("theme","color")
a = 1
