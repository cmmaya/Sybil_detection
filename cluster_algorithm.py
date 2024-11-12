import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community.community_louvain as community_louvain
import numpy as np
import tqdm
import igraph as ig
import leidenalg

def cluster_algorithm(transactions_df):
    initial_lenght = len(transactions_df)

    # Load Ethereum transactions and blacklist
    blacklist = pd.read_csv("data/blacklist.csv")
    blacklist.columns = ['address']
    # Create a filtered transactions DataFrame
    transactions_df = transactions_df[
        ~(transactions_df['from'].isin(blacklist['address'])) &
        ~(transactions_df['to'].isin(blacklist['address']))
    ]
    print("Trx before filtering: ", initial_lenght, "\Trx after filtering blacklisted: ", len(transactions_df))

    # Create a directed graph from the transaction data
    G_nx = nx.from_pandas_edgelist(transactions_df, source="from", target="to", create_using=nx.DiGraph())

    # Convert NetworkX graph to iGraph format for Leiden algorithm
    G = ig.Graph.TupleList(G_nx.edges(), directed=True)

    # Apply the Leiden algorithm to detect communities
    partition = leidenalg.find_partition(G, leidenalg.ModularityVertexPartition)

    # Map partition results back to NetworkX nodes
    partition_dict = {node: community for node, community in zip(G.vs["name"], partition.membership)}

    # Save the partition DataFrame to CSV
    partition_df = pd.DataFrame(list(partition_dict.items()), columns=["Account", "Cluster_ID"])

    # Identify clusters with more than 20 members
    clusters = partition_df.groupby("Cluster_ID")["Account"].apply(list).to_dict()

    large_clusters = {cid: members for cid, members in clusters.items() if len(members) > 15}

    # Initialize a set to store all members of large clusters and their connected clusters
    connected_members = set()

    # Iterate through each large cluster
    for _ , large_cluster_members in tqdm.tqdm(large_clusters.items()):
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
    print('Lenght: ',len(connected_members_list))

    return partition_dict, connected_members_list, G_nx