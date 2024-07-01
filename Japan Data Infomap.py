#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 09:19:29 2024

@author: seychellebrainard
"""

import os
import networkx as nx
from infomap import Infomap
import matplotlib.colors as mcolors
import folium
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
# markov_time: Scales link flow to change the cost of moving between modules. Higher values results in fewer modules.
# teleportation_prob: Probability of teleporting to a random node or link.
im = Infomap(directed=True, two_level=True , markov_time=5, teleportation_probability=0.001, num_trials=4) #markov 5 = 25
# im=Infomap(directed=True) --> clusters = 4


# Create a map from node identifiers to integers
node_mapping = {node: i for i, node in enumerate(ds.nodes())}
    
# Add edges to Infomap with mapped integer identifiers
for source_node, target_node, edge_data in ds.edges(data=True):
    source = node_mapping[source_node]
    target = node_mapping[target_node]
    weight = edge_data.get('weight', 1.0)  # Default weight to 1.0 if not present
    im.addLink(source, target, weight)

# Run Infomap
im.run()

#get clusters
clusters = im.getModules()

#get the lat and lon data for each node and center the map on the region
latitudes = [ds.nodes[node]['latitude'] for node in ds.nodes()]
longitudes = [ds.nodes[node]['longitude'] for node in ds.nodes()]
map_center = [sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)]

#creat folium map
m = folium.Map(location=(map_center), zoom_start=8, tiles="cartodb positron")

# Create a color map
colors = list(mcolors.CSS4_COLORS.keys())
unique_clusters = set(clusters.values())
color_map = {cluster: mcolors.to_hex(mcolors.CSS4_COLORS[colors[i % len(colors)]]) for i, cluster in enumerate(unique_clusters)}

# Assign colors to nodes based on their community
node_colors = [color_map[clusters[node_mapping[node]]] for node in ds.nodes()]

#create a feature group of the nodes to add to the map
coral = folium.map.FeatureGroup()

#add each node to the feature group
for lat, lon, color in zip(latitudes, longitudes, node_colors):
    coral.add_child(
        folium.features.CircleMarker(
            [lat, lon],
            radius=2, # define how big you want the circle markers to be
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6
        )
    )

#add the feature group to the mpa
m.add_child(coral)
m.save("coral connectivity.html")

