#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 09:26:14 2024

@author: seychellebrainard
"""

import os
import networkx as nx
from infomap import Infomap
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

#get data
cwd = os.getcwd()
fh = cwd + '/static_matrix.graphml'
ds = nx.read_graphml(fh)

#initalize the infomap 
im = Infomap()

# Create a mapping from node identifiers to integers
node_mapping = {node: i for i, node in enumerate(ds.nodes())}


# Add edges to Infomap with mapped integer identifiers
for edge in ds.edges():
    im.addLink(node_mapping[edge[0]], node_mapping[edge[1]])

# Run Infomap
im.run()

# Get the communities
communities = im.getModules()

# Reverse the node mapping to get original node identifiers
reverse_node_mapping = {v: k for k, v in node_mapping.items()}

# Create a color map
colors = list(mcolors.TABLEAU_COLORS.keys())
color_map = {community: colors[i % len(colors)] for i, community in enumerate(set(communities.values()))}


# Assign colors to nodes based on their community
node_colors = [color_map[communities[node]] for node in node_mapping.values()]

# Extract geographic coordinates (assuming they are stored as node attributes 'lat' and 'lon')
pos = {node: (ds.nodes[node]['longitude'], ds.nodes[node]['latitude']) for node in ds.nodes()}

# Draw the graph with geographic positions
plt.figure(figsize=(15, 15))

nx.draw_networkx_nodes(ds, pos, node_color=node_colors, node_size=20, alpha=0.7)
#nx.draw_networkx_edges(ds, pos, alpha=0.5)
#nx.draw_networkx_labels(ds, pos, font_size=8, font_color='black', font_weight='bold')

plt.title('Community Detection with Infomap (Geographic Layout)')
plt.show()





