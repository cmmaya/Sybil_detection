import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from node2vec import Node2Vec
from sklearn.cluster import DBSCAN
import numpy as np

# Load the transaction data
transactions_df = pd.read_csv("data/transactions.csv")

# Create a directed graph from the transaction data
G = nx.from_pandas_edgelist(transactions_df, source="from", target="to", create_using=nx.DiGraph())

# Generate node embeddings using node2vec
node2vec = Node2Vec(G, dimensions=64, walk_length=30, num_walks=200, workers=4)
model = node2vec.fit(window=10, min_count=1)

# Extract embeddings for each node in the graph
node_embeddings = np.array([model.wv[node] for node in G.nodes()])
node_labels = list(G.nodes())

# Apply DBSCAN clustering on the node embeddings
dbscan = DBSCAN(eps=1.0, min_samples=5)  # Adjust `eps` and `min_samples` based on your data characteristics
cluster_labels = dbscan.fit_predict(node_embeddings)

# Create a DataFrame for cluster assignments and save it
cluster_df = pd.DataFrame({"Account": node_labels, "Cluster_ID": cluster_labels})
cluster_df.to_csv("data/dbscan_clusters.csv", index=False)
print("DBSCAN clusters saved to data/dbscan_clusters.csv")

# Identify unique clusters (excluding noise points with Cluster_ID == -1) and assign colors
unique_clusters = [label for label in set(cluster_labels) if label != -1]
colors = plt.cm.tab20.colors  # Distinct colors for each cluster
cluster_colors = {cluster: colors[i % len(colors)] for i, cluster in enumerate(unique_clusters)}

# Set up positions for each cluster to separate them in the plot
cluster_centers = {cluster: (np.cos(2 * np.pi * i / len(unique_clusters)) * 5,
                             np.sin(2 * np.pi * i / len(unique_clusters)) * 5)
                   for i, cluster in enumerate(unique_clusters)}

# Initialize the positions dictionary
pos = {}

# Arrange each cluster around its cluster center
for cluster_id, center in cluster_centers.items():
    # Extract nodes in the current cluster
    cluster_nodes = [node for node, label in zip(node_labels, cluster_labels) if label == cluster_id]
    subgraph = G.subgraph(cluster_nodes)
    
    # Generate positions for the cluster and offset by the cluster center
    cluster_pos = nx.spring_layout(subgraph, seed=42, k=0.2, scale=1.0)
    cluster_pos = {node: (coord[0] + center[0], coord[1] + center[1]) for node, coord in cluster_pos.items()}
    
    # Update main position dictionary
    pos.update(cluster_pos)

# Plot all clusters in a single graph with separation
plt.figure(figsize=(14, 14))

# Draw nodes with colors based on their cluster, excluding noise points
for node, cluster_id in zip(node_labels, cluster_labels):
    if cluster_id != -1:  # Ignore noise points with cluster ID -1
        nx.draw_networkx_nodes(G, pos, nodelist=[node], node_size=50, node_color=[cluster_colors[cluster_id]])

# Filter edges to include only those where both nodes are in pos
filtered_edges = [(u, v) for u, v in G.edges() if u in pos and v in pos]

# Draw edges with arrows and reduced alpha
nx.draw_networkx_edges(G, pos, edgelist=filtered_edges, edge_color="gray", alpha=0.5, arrows=True)


# Show the plot
plt.title("DBSCAN Community Detection on Transaction Network with Separate Clusters")
plt.savefig("images/DBSCAN.png", format='png')  # Save as PNG file
plt.show()
