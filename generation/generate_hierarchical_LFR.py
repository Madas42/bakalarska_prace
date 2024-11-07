from graphgen.lfr_generators import weighted_directed_lfr_as_nx
from graphgen.lfr_generators import weighted_undirected_lfr_as_nx
from graphgen.lfr_generators import unweighted_directed_lfr_as_nx
from graphgen.lfr_generators import unweighted_undirected_lfr_as_nx

import networkx as nx

def convert_tuple_to_string(g):
    for node, data in g.nodes(data=True):
        for key, value in data.items():
            if isinstance(value, tuple):
                data[key] = str(value)

    for u, v, data in g.edges(data=True):
        for key, value in data.items():
            if isinstance(value, tuple):
                data[key] = str(value)

def generate_weighted_directed_lfr(num_nodes, average_k, max_degree, mut, muw, com_size_min, com_size_max, seed):
    g = weighted_directed_lfr_as_nx(num_nodes = num_nodes,
                                    average_k = average_k,
                                    max_degree = max_degree,
                                    mut = mut,
                                    muw = muw,
                                    com_size_min = com_size_min,
                                    com_size_max = com_size_max,
                                    seed = seed)

    # Convert tuple data values to strings
    convert_tuple_to_string(g)

    return g

def generate_weighted_undirected_lfr(num_nodes, average_k, max_degree, mut, muw, com_size_min, com_size_max, seed):
    g = weighted_undirected_lfr_as_nx(num_nodes = num_nodes,
                                    average_k = average_k,
                                    max_degree = max_degree,
                                    mut = mut,
                                    muw = muw,
                                    com_size_min = com_size_min,
                                    com_size_max = com_size_max,
                                    seed = seed)

    # Convert tuple data values to strings
    convert_tuple_to_string(g)

    return g

def generate_unweighted_directed_lfr(num_nodes, average_k, max_degree, mu, com_size_min, com_size_max, seed):
    g = unweighted_directed_lfr_as_nx(num_nodes = num_nodes,
                                    average_k = average_k,
                                    max_degree = max_degree,
                                    mu = mu,
                                    com_size_min = com_size_min,
                                    com_size_max = com_size_max,
                                    seed = seed)

    # Convert tuple data values to strings
    convert_tuple_to_string(g)

    return g

def generate_unweighted_undirected_lfr(num_nodes, average_k, max_degree, mu, com_size_min, com_size_max, seed):
    g = unweighted_undirected_lfr_as_nx(num_nodes = num_nodes,
                                    average_k = average_k,
                                    max_degree = max_degree,
                                    mu = mu,
                                    com_size_min = com_size_min,
                                    com_size_max = com_size_max,
                                    seed = seed)

    # Convert tuple data values to strings
    convert_tuple_to_string(g)

    return g
