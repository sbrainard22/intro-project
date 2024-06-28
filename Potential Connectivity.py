#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:38:29 2024

@author: seychellebrainard
"""

import os
import networkx as nx
from infomap import Infomap
import matplotlib.colors as mcolors
import folium

#get data
cwd = os.getcwd()
fh = cwd + '/static_matrix.graphml'
ds = nx.read_graphml(fh)

#remove nodes with no coral cover
to_remove = []
for node, data in ds.nodes(data=True):
    if data['coral_cover'] == 0:
        to_remove.append(node)
ds.remove_nodes_from(to_remove)

#initalize the infomap 
im=Infomap()

# Create a map from node identifiers to integers
node_mapping = {node: i for i, node in enumerate(ds.nodes())}

#add edges to infomap
for edge in ds.edges(data=True):
    im.addLink(node_mapping[edge[0]], node_mapping[edge[1]])


# Run Infomap
im.run()

#get clusters
clusters = im.getModules()

# Define the cluster of interest
cluster_of_interest = 1




# Identify nodes in the cluster of interest
#nodes_in_cluster = [node for node, cluster in clusters.items() if cluster == cluster_of_interest]

# Filter the edges to include only those where both nodes are in the cluster of interest
#edges_in_cluster = [(source, target, data) for source, target, data in ds.edges(data=True) if source in nodes_in_cluster and target in nodes_in_cluster]

#create a list of the coral cover for each node
coral_cover = [ds.nodes[node]['coral_cover'] for node in ds.nodes()]

#create dictionaries to store 
weight_dic = {}
#edge_coral = {}
potential_con = {}

for source_node, target_node, edge_data in ds.edges(data=True):
    source = node_mapping[source_node]
    target = node_mapping[target_node]
    weight = edge_data.get('weight')
    keys = (source, target)
    weight_dic.update({keys: weight})
   # edge_coral.update({coral_cover[source]: weight})
    potential_connectivity = weight/coral_cover[source]
    potential_con.update({keys: potential_connectivity})
    
    


    

    
    
    
    
    
    
    
    
    
    