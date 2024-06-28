#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:15:38 2024

@author: seychellebrainard
"""

import os
import networkx as nx
from infomap import Infomap
from pyvis.network import Network

# Get data
cwd = os.getcwd()
fh = os.path.join(cwd, 'static_matrix.graphml')
ds = nx.read_graphml(fh)

net = Network()
net.barnes_hut()

# Remove all nodes with no coral cover
to_remove = [node for node, data in ds.nodes(data=True) if data['coral_cover'] == 0]
ds.remove_nodes_from(to_remove)

# Initialize Infomap
im = Infomap(directed=True, two_level=True)

# Create a map from node identifiers to integers
node_mapping = {node: i for i, node in enumerate(ds.nodes())}

# Add edges to Infomap with mapped integer identifiers
for edge in ds.edges():
    im.addLink(node_mapping[edge[0]], node_mapping[edge[1]])

# Run Infomap
im.run()

# Get the communities
clusters = im.getModules()

# Reverse the node mapping to get original node identifiers
reverse_node_mapping = {v: k for k, v in node_mapping.items()}

# Retain only nodes in cluster 1
cluster_1_nodes = [reverse_node_mapping[node] for node, cluster in clusters.items() if cluster == 1]
cluster_1_subgraph = ds.subgraph(cluster_1_nodes).copy()

# Get the lat and lon data for each node in cluster 1 and center the map on the region
latitudes = [cluster_1_subgraph.nodes[node]['latitude'] for node in cluster_1_subgraph.nodes()]
longitudes = [cluster_1_subgraph.nodes[node]['longitude'] for node in cluster_1_subgraph.nodes()]
map_center = [sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)]

# Create a list of the coral cover for each node
coral_cover = {node: cluster_1_subgraph.nodes[node]['coral_cover'] for node in cluster_1_subgraph.nodes()}

# Create dictionaries to store 
weight_dic = {}
potential_con = {}
source_reef = []
target_reef = []
pc = []

for source_node, target_node, edge_data in cluster_1_subgraph.edges(data=True):
    weight = edge_data.get('weight', 1)  # Default weight to 1 if not present
    keys = (source_node, target_node)
    weight_dic[keys] = weight
    potential_connectivity = weight / coral_cover[source_node]
    potential_con[keys] = potential_connectivity
    source_reef.append(source_node)
    target_reef.append(target_node)
    pc.append(potential_connectivity)

sources = source_reef
targets = target_reef
weights = pc

edge_data = zip(sources, targets, weights)

for e in edge_data:
                src = e[0]
                dst = e[1]
                w = e[2]
                net.add_node(src, src, title=src)
                net.add_node(dst, dst, title=dst)
                net.add_edge(src, dst, value=w)
                
net.show('pc network.html')




