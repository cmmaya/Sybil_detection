### Description

Sybil detection can be attacked using clustering algortihms to detect communities of accounts following basic patterns. These patterns can be either Star-like or Line-like shaped.

**_Transactions simulation_**
Transactions are simulated in the `transaction_simulation.py` file. The logic operates as follows: starting with a set number of initial accounts, each account has a 30% probability of initating a patterned transaction. This transaction pattern can either be a `star` or a `line`, involving 5 to 10 additional branched accounts. For each new member account, this process is repeated up to a specified maximum depth.

**_Clustering Algorithms_**
To detect communities in a large networks, we test the following algorithms:

- **Louvain**: It’s based on modularity optimization, which aims to divide a network into clusters (or communities) that maximize the number of edges within clusters while minimizing the number of edges between them.
- **Leiden**: It improves on Louvain in terms of both speed and accuracy. It addresses some limitations of Louvain, such as potentially getting stuck in local optima that lead to disconnected communities or poor modularity.
- **DBSCAN**: Clusters nodes based on the density of their connections. It’s a good choice for finding communities in networks where there are dense regions and less dense or noisy points

**Post-clustering**: After applying the clustering method, communities with size +15 members are analysed to see the connected subclusters with less than 15 members and count the total accounts. Then the number is evaluated based on the number of sybil accounts obtained in the simulation.

**TODO**: 
- Find state of the art clustering techniques
- Cluster time and amount from transaction's info.
