import networkx as nx
import numpy as np
import scipy.sparse as sp


def remove_self_loops(G):
    """
    Returns copy of graph without selfloops
    """
    A = np.asarray(nx.adjacency_matrix(G).toarray())
    np.fill_diagonal(A, 0)
    G = nx.from_numpy_array(A, create_using=nx.DiGraph)

    return G


def adjacency_to_binary(A):
    """
    Computes binarised adjacency matrix
    """

    A_binary = sp.lil_matrix(A.shape)
    A_binary[A > 0] = 1

    return A_binary


def visualse_largest_components(G):
    """
    input: network G
    output: function computed indicator for nodes in LSCC and LWCC
    """

    n_nodes = len(list(G.nodes()))
    node_dict = {list(G.nodes)[i]: i for i in range(n_nodes)}

    # Compute weakly connected components of G
    wcc_set = list(nx.weakly_connected_components(G))
    n_wcc = len(list(wcc_set))

    # Store component label for each node in G
    wcc_id = np.zeros(n_nodes, dtype=int)

    # Repeat for each community k
    for k in range(0, n_wcc):
        # Nodes of the k-th component are marked with k
        nodes = list(wcc_set[k])
        for node in nodes:
            wcc_id[node_dict[node]] = k

    # Compute sizes of each component
    unordered_counts = np.histogram(wcc_id, bins=np.arange(0, n_wcc + 1))[0]
    # Get component indices sorted according to size
    component_ranked = np.argsort(-unordered_counts)
    # Create dictionary that describes map from old labels to new labels
    rank = {component_ranked[k]: k for k in range(0, n_wcc)}
    # Apply permutation to labels
    wcc_id_ranked = wcc_id.copy()
    for i in range(0, len(wcc_id_ranked)):
        wcc_id_ranked[i] = rank[wcc_id_ranked[i]]

    # Get indicator for LWCC
    ind_lwcc = np.asarray(wcc_id_ranked == 0, dtype="int")

    # Compute strongly connected comoonents of G
    scc_set = list(nx.strongly_connected_components(G))
    n_scc = len(list(scc_set))

    # Store component label for each node in G
    scc_id = np.zeros(n_nodes, dtype=int)

    # Repeat for each community k
    for k in range(0, n_scc):
        # Nodes of the k-th component are marked with k
        nodes = list(scc_set[k])
        for node in nodes:
            scc_id[node_dict[node]] = k

    # Compute sizes of each component
    unordered_counts = np.histogram(scc_id, bins=np.arange(0, n_scc + 1))[0]
    # Get component indices sorted according to size
    component_ranked = np.argsort(-unordered_counts)
    # Create dictionary that describes map from old labels to new labels
    rank = {component_ranked[k]: k for k in range(0, n_scc)}
    # Apply permutation to labels
    scc_id_ranked = scc_id.copy()
    for i in range(0, len(scc_id_ranked)):
        scc_id_ranked[i] = rank[scc_id_ranked[i]]

    ind_lscc = np.asarray(scc_id_ranked == 0, dtype="int")

    return ind_lwcc + ind_lscc


def compute_coverage(G, H, intra=True):
    """
    Input: Graph G, indicator matrix H
    Output: TFC of partition if intra is True, otherwise IFC
    """

    A = nx.adjacency_matrix(G).toarray()

    if intra == False:
        np.fill_diagonal(A, 0)

    flow_within = np.trace(H.transpose().dot(A).dot(H))
    total_flow = A.sum()

    return flow_within / total_flow


def compute_coverage_community(G, H, intra=True):
    """
    Input: Graph G, indicator matrix H
    Output: TFC for each community if intra is True, otherwise IFC
    """

    coverage = []
    A = nx.adjacency_matrix(G).toarray()
    if intra == False:
        np.fill_diagonal(A, 0)

    for k in range(H.shape[1]):

        flow_within = H.transpose().dot(A).dot(H)[k, k]
        total_flow = H.transpose().dot(A)[k, :].sum()

        # # coverage is 1 if there is no flow
        # if total_flow == 0:
        #     coverage.append(1)
        # else:
        #     coverage.append(flow_within / total_flow)
        coverage.append(flow_within / total_flow)

    return np.asarray(coverage)


def compute_indicator_matrix(node_ids):
    """
    Input: Vector of node_ids for partition
    Output: Indicator matrix H corresponding to partition
    """

    N = len(node_ids)
    c = max(node_ids)
    H = np.zeros([N, c + 1], dtype=int)
    for i in range(N):
        H[i, node_ids[i]] = 1

    return H


def node_id_to_dict(G, node_id):
    """
    Input: Graph G and array of node_id's
    Output: Dictionary that maps community number to node_keys
    """
    node_keys = list(G.nodes())
    n_communities = np.max(node_id)
    community_dict = {}
    for i in range(n_communities + 1):
        c = np.argwhere(node_id == i).flatten()
        c_set = set(node_keys[j] for j in c)
        if len(c) > 0:
            # community_dict[node_id[i]] = c_set -> bug!!
            community_dict[i] = c_set
    return community_dict


def compute_nodal_containment(G, node_ids):
    """
    Input: Graph G and node_ids for partition
    Output: Vector of containment proportions of flows within communities
    """

    N = len(node_ids)

    # Get indicator matrix
    H = compute_indicator_matrix(node_ids)

    # Get adjacency matrix without self-loops
    A = nx.adjacency_matrix(G).toarray()
    np.fill_diagonal(A, 0)

    # Compute flows from nodes to communities
    out_flows = A.dot(H)
    out_flows_within = np.asarray([out_flows[i, node_ids[i]] for i in range(N)])

    # Compute node out-degree
    d = A.dot(np.ones(N))

    # Return proportion
    return out_flows_within / d
