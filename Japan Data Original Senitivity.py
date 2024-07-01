#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:07:27 2024

@author: seychellebrainard
"""

import os
import networkx as nx
from infomap import Infomap
from collections import Counter
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from collections import Counter


# Get data
cwd = os.getcwd()
fh = os.path.join(cwd, 'static_matrix.graphml')
ds = nx.read_graphml(fh)

# Remove all nodes with no coral cover
to_remove = [node for node, data in ds.nodes(data=True) if data['coral_cover'] == 0]
ds.remove_nodes_from(to_remove)

# Create a map from node identifiers to integers
node_mapping = {node: i for i, node in enumerate(ds.nodes())}

# Function to run Infomap and get clusters
def run_infomap(ds, num_trials):
    im = Infomap(directed=True, two_level=True, markov_time=5, teleportation_probability=0.001, num_trials=num_trials)
    for edge in ds.edges(data=True):
        im.addLink(node_mapping[edge[0]], node_mapping[edge[1]])
    im.run()
    clusters = im.getModules()
    cluster_assignment = [clusters[node_mapping[node]] for node in ds.nodes()]
    cluster_counts = Counter(cluster_assignment)
    return cluster_assignment, cluster_counts

# Run Infomap for different num_trials values and store the results
num_trials_values = range(1, 15, 1)
clusterings = []
cluster_counts_per_trial = []

#run infomap for each num_trials_values
for num_trials in num_trials_values:
    clusters, cluster_counts = run_infomap(ds, num_trials)
    clusterings.append(clusters)
    cluster_counts_per_trial.append(cluster_counts)

# Compare clusterings using Adjusted Rand Index (ARI) and Normalized Mutual Information (NMI)
ari_scores = [] # a measure of the similarity between two data clusterings
nmi_scores = [] #  scale the results between 0 (no mutual information) and 1 (perfect correlation)

# calculate ari and nmi for each num_trials
for i in range(1, len(clusterings)):
    ari = adjusted_rand_score(clusterings[i-1], clusterings[i])
    nmi = normalized_mutual_info_score(clusterings[i-1], clusterings[i])
    ari_scores.append(ari)
    nmi_scores.append(nmi)

# Print results
for i, num_trials in enumerate(num_trials_values[1:]):
    print(f'num_trials: {num_trials}, ARI: {ari_scores[i]}, NMI: {nmi_scores[i]}')
    #print(f'Cluster counts for num_trials {num_trials}: {dict(cluster_counts_per_trial[i])}')

# Determine the stability point
stability_threshold = 0.99  # Define a threshold for stability
stable_index = next(i for i, score in enumerate(nmi_scores) if score >= stability_threshold)
stable_num_trials = num_trials_values[stable_index + 1]

print(f'The network clustering becomes stable at num_trials = {stable_num_trials}')
            