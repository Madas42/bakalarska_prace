import networkx as nx
import random

def ravasz_barabasi_generator(n, m, levels, mu, tau1, tau2, min_cluster_size, progress_callback=None):
    """
    Generate a Ravasz-Barabási hierarchical network with specified parameters.

    Parameters:
    - n: Total number of nodes
    - m: Number of edges to attach from a new node to existing nodes
    - levels: Number of hierarchical levels
    - mu: Probability of a node belonging to multiple clusters
    - tau1: Parameter to control the distribution of cluster sizes
    - tau2: Parameter to control the preferential attachment for degree distribution
    - min_cluster_size: Minimum size of each cluster
    - progress_callback: Function to call to update progress

    Returns:
    - G: Generated Ravasz-Barabási network
    """
    # Initialize an empty graph
    G = nx.Graph()

    # Create initial cluster (root)
    G.add_node(0, community=[0])
    current_node = 1

    total_steps = levels + n  # Total steps for progress calculation
    current_step = 0

    # Generate hierarchical levels
    for level in range(levels):
        # Determine the number of nodes at this level
        nodes_in_level = min(n - current_node, 2 ** level)

        # Calculate cluster sizes based on tau1
        cluster_sizes = [
            max(min_cluster_size, int(random.paretovariate(tau1)))
            for _ in range(nodes_in_level)
        ]

        # Add nodes for this level and create clusters
        clusters = []
        for size in cluster_sizes:
            cluster = list(range(current_node, current_node + size))
            for node in cluster:
                G.add_node(node, community=[level])
            clusters.append(cluster)
            current_node += size

        # Connect nodes within clusters
        for cluster in clusters:
            # Ensure the cluster has at least one node
            if len(cluster) > 1:
                for i in range(len(cluster)):
                    for j in range(i + 1, len(cluster)):
                        if random.random() < mu:  # Intra-cluster probability
                            G.add_edge(cluster[i], cluster[j])

        # Connect new nodes to existing nodes
        existing_nodes = list(G.nodes())[:-nodes_in_level]  # Nodes from previous levels

        for new_node in range(current_node - nodes_in_level, current_node):
            # Select m existing nodes based on preferential attachment using tau2
            degree_dict = dict(G.degree(existing_nodes))
            total_degree = sum(degree_dict.values())

            if total_degree == 0:
                # Assign equal probabilities if total_degree is zero
                probabilities = [1 / len(existing_nodes) for _ in existing_nodes]
            else:
                probabilities = [(degree_dict[node] ** tau2) / total_degree for node in existing_nodes]

            targets = random.choices(existing_nodes, weights=probabilities, k=m)
            G.add_edges_from((new_node, target) for target in targets)

            # Update progress for each new node
            current_step += 1
            if progress_callback:
                progress_callback(current_step / total_steps * 100)

    return G