#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 09:50:38 2024

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

#initalize the infomap 
im = Infomap(directed=True, two_level=True, markov_time=1, teleportation_probability=0.001, num_trials=50)

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
reverse_node_mapping = {v: k for k, v in node_mapping.items()} #dictionary allows you to look up the original node identifier given its integer identifier.

#get the lat and lon data for each node and center the map on the region
latitudes = [ds.nodes[node]['latitude'] for node in ds.nodes()]
longitudes = [ds.nodes[node]['longitude'] for node in ds.nodes()]
map_center = [sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)]

#creat folium map
m = folium.Map(location=(map_center), zoom_start=8, tiles="cartodb positron")

# Create a color map
colors = list(mcolors.TABLEAU_COLORS.keys())
color_map = {cluster: mcolors.to_hex(mcolors.TABLEAU_COLORS[colors[i % len(colors)]]) for i, cluster in enumerate(set(clusters.values()))}

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
m.save("first infomap.html")


