import pandas as pd
import networkx as nx

# Load transactions and partition data from CSV
df_transactions = pd.read_csv("data/transactions.csv")
df_partition = pd.read_csv("data/partition_clusters.csv")

# Rebuild the graph from transactions
G = nx.from_pandas_edgelist(df_transactions, "from", "to", create_using=nx.Graph())

# Reconstruct clusters from the partition data
clusters = df_partition.groupby("Cluster_ID")["Account"].apply(list).to_dict()

# Identify clusters with more than 20 members
large_clusters = {cid: members for cid, members in clusters.items() if len(members) > 15}

# Initialize a set to store all members of large clusters and their connected clusters
connected_members = set()

# Iterate through each large cluster
for large_cluster_id, large_cluster_members in large_clusters.items():
    # Add all members of the large cluster to the set
    connected_members.update(large_cluster_members)
    
    # Check connections between large cluster members and other clusters
    for member in large_cluster_members:
        # Find neighbors of the current member in the graph
        neighbors = list(G.neighbors(member))
        
        # Check if neighbors belong to other clusters
        for neighbor in neighbors:
            for cluster_id, cluster_members in clusters.items():
                # If the neighbor belongs to another cluster, add all its members
                if neighbor in cluster_members and cluster_id not in large_clusters:
                    connected_members.update(cluster_members)
                    break  # Move to next neighbor once the cluster is found

# Convert the connected members set to a list
connected_members_list = list(connected_members)

# Output the combined list of members
# print("Combined list of members from large clusters and connected clusters:")
# print(connected_members_list)
print('Lenght: ',len(connected_members_list))
