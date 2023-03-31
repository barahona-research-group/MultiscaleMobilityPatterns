import numpy as np
import networkx as nx
import scipy.sparse as sp
import pickle
from pygenstability import run, constructors
from functools import partial

import sys
from pathlib import Path

path = str(Path.cwd().parents[0])
root_processed = path + "/MultiscaleMobilityPatterns/data/processed/"
root_networks = path + "/MultiscaleMobilityPatterns/data/processed/networks/"

##############################
# Generate DiGraph from data #
##############################

# Load data (deserialize)
with open(root_networks + "base_network_lscc.npz", "rb") as handle:
    lscc_dict = pickle.load(handle)

# Create LSCC DiGraph
lscc = nx.from_dict_of_dicts(lscc_dict, create_using=nx.DiGraph)

# Compute adjacency matrix and node list of LSCC
A_LSCC = nx.adjacency_matrix(lscc)
lscc_nodes_list = np.asarray(list(lscc.nodes()))
s_lscc = len(lscc_nodes_list)

# Subtract self-loops
B_LSCC_array = A_LSCC - np.diag(np.diag(A_LSCC.toarray()))
B_LSCC = sp.csr_matrix(B_LSCC_array)


##########
# Run MS #
##########

# define parameters
n_scale = 300
min_scale = -2
max_scale = 3
n_tries = 300
n_NVI = 30
n_workers = 2  # 20
result_file = root_processed + "MS_results.pkl"

# defining the constructor externally
directed_constructor = constructors.constructor_directed(
    B_LSCC, exp_comp_mode="expm", kwargs={"alpha": 1}
)

# run Markov Stability analysis
all_results = run(
    B_LSCC,
    constructor=directed_constructor,
    min_scale=min_scale,
    max_scale=max_scale,
    n_scale=n_scale,
    n_tries=n_tries,
    n_NVI=n_NVI,
    n_workers=n_workers,
    exp_comp_mode="expm",
    result_file=result_file,
)
