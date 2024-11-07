import numpy as np


def generate_stochastic_block(num_nodes, num_groups, seed=None):
    """
    Generate a hierarchical network using graph-tool's stochastic block model.

    :param num_nodes (int):         Number of nodes in the network.
    :param num_groups (int):        Number of groups for the hierarchical structure.
    :param seed (int, optional):    Seed for random number generator for reproducibility.

    :return Graph:                  Generated hierarchical network.
    """
    # Set the seed for reproducibility
    if seed is not None:
        np.random.seed(seed)

    # Create a random graph with num_nodes nodes
    g = Graph(directed=False)
    g.add_edge_list(np.random.randint(0, num_nodes, size=(num_nodes, 2)))

    # Assign nodes to groups using the stochastic block model
    state = minimize_blockmodel_dl(g, B=num_groups)

    # Draw the hierarchical network
    pos = sfdp_layout(g)
    draw_hierarchy(state, pos, output_size=(1000, 1000), output="hierarchical_network.png")

    return g