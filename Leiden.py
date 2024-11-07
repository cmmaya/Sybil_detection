import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import igraph as ig
import leidenalg

# Load the transaction data
transactions_df = pd.read_csv("data/transactions.csv")

# Create a directed graph from the transaction data
G_nx = nx.from_pandas_edgelist(transactions_df, source="from", target="to", create_using=nx.DiGraph())

# Convert NetworkX graph to iGraph format for Leiden algorithm
G_ig = ig.Graph.TupleList(G_nx.edges(), directed=True)

# Apply the Leiden algorithm to detect communities
partition = leidenalg.find_partition(G_ig, leidenalg.ModularityVertexPartition)

# Map partition results back to NetworkX nodes
partition_dict = {node: community for node, community in zip(G_ig.vs["name"], partition.membership)}

# Save the partition DataFrame to CSV
partition_df = pd.DataFrame(list(partition_dict.items()), columns=["Account", "Cluster_ID"])
partition_df.to_csv("data/partition_clusters_leiden.csv", index=False)
print("Partition clusters saved to data/partition_clusters_leiden.csv")

# Identify unique communities and assign colors
unique_communities = list(set(partition_dict.values()))
colors = plt.cm.tab20.colors  # Distinct colors for each community
community_colors = {community: colors[i % len(colors)] for i, community in enumerate(unique_communities)}

# Set up cluster centers for each community to reduce overlap
cluster_centers = {community: (np.cos(2 * np.pi * i / len(unique_communities)) * 5,
                               np.sin(2 * np.pi * i / len(unique_communities)) * 5)
                   for i, community in enumerate(unique_communities)}

# Initialize the positions dictionary
pos = {}

# Arrange each community around its cluster center
for community_id, center in cluster_centers.items():
    # Extract nodes in the current community
    community_nodes = [node for node, comm in partition_dict.items() if comm == community_id]
    subgraph = G_nx.subgraph(community_nodes)
    
    # Generate positions for the community within a smaller layout and offset by the cluster center
    community_pos = nx.spring_layout(subgraph, seed=42, k=0.2, scale=1.0)
    community_pos = {node: (coord[0] + center[0], coord[1] + center[1]) for node, coord in community_pos.items()}
    
    # Update main position dictionary
    pos.update(community_pos)

# Plot all communities in a single graph with separation
plt.figure(figsize=(14, 14))

# Draw nodes with colors based on their community
for node, community_id in partition_dict.items():
    nx.draw_networkx_nodes(G_nx, pos, nodelist=[node], node_size=50, node_color=[community_colors[community_id]])

# Draw edges with arrows and reduced alpha
nx.draw_networkx_edges(G_nx, pos, edge_color="gray", alpha=0.5, arrows=True)

# Show the plot
plt.title("Leiden Community Detection on Transaction Network with Separate Clusters")
plt.savefig("images/Leiden.png", format='png')  # Save as PNG file
plt.show()
