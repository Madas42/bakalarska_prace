from graphgen.lfr_generators import weighted_directed_lfr_graph
import networkx as nx


def generate_barabasi_albert(num_nodes, branching_factor, seed = 42):
    """
    Generate a hierarchical network using the Barabasi-Albert model.
    :param num_nodes:           Number of nodes in the network
    :param branching_factor:    Number of edges to attach from a new node to existing nodes
    :param seed:                Seed for random number generator
    :return G:                  Networkx graph
    """

    G = nx.barabasi_albert_graph(num_nodes, branching_factor, seed)

    return G