#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 09:14:30 2024

@author: seychellebrainard
"""

import os
import networkx as nx
from infomap import Infomap
import matplotlib.colors as mcolors
import folium

# Get data
cwd = os.getcwd()
fh = os.path.join(cwd, 'static_matrix.graphml')
ds = nx.read_graphml(fh)

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

# Create Folium map
m = folium.Map(location=map_center, zoom_start=8, tiles="cartodb positron")

# Create a color map
colors = list(mcolors.TABLEAU_COLORS.keys())
color_map = {cluster: mcolors.to_hex(mcolors.TABLEAU_COLORS[colors[i % len(colors)]]) for i, cluster in enumerate(set(clusters.values()))}

# Assign colors to nodes in cluster 1 based on their community
node_colors = [color_map[clusters[node_mapping[node]]] for node in cluster_1_subgraph.nodes()]

# Create a feature group of the nodes to add to the map
coral = folium.map.FeatureGroup()

# Add each node in cluster 1 to the feature group
for node, color in zip(cluster_1_subgraph.nodes(data=True), node_colors):
    coral.add_child(
        folium.features.CircleMarker(
            [node[1]['latitude'], node[1]['longitude']],
            radius=2,  # Define the size of the circle markers
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6
        )
    )

# Add the feature group to the map
m.add_child(coral)
m.save("sanity_check.html")