import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import hashlib
import os
import utils

def generate_hash():
    """Generate a random unique hash for each account."""
    return hashlib.sha256(str(random.randint(1, int(1e9))).encode()).hexdigest()


def generate_star_pattern(center_account):
    """Generate a star pattern with a random number of accounts (5 to 10) from the central account."""
    star_transactions = []
    num_branches = random.randint(5, 10)
    for _ in range(num_branches):
        branch_account = generate_hash()
        star_transactions.append((center_account, branch_account))
    return star_transactions

def generate_line_pattern(start_account, chain_length):
    """Generate a line pattern starting from a given account with a specified chain length."""
    line_transactions = []
    previous_account = start_account
    for _ in range(chain_length):
        next_account = generate_hash()
        line_transactions.append((previous_account, next_account))
        previous_account = next_account
    return line_transactions

def generate_nested_patterns(start_account, max_depth, depth=1):
    """
    Generate nested star and line patterns starting from a given account,
    with a 30% chance for each account to start a new pattern up to a max depth.
    If a pattern is not initiated, generate a normal transaction.
    """
    transactions = []
    
    if depth > max_depth:
        return transactions

    # 30% chance to initiate a pattern
    if random.random() < 0.3:
        pattern_type = random.choice(["star", "line"])
        
        if pattern_type == "star":
            new_transactions = generate_star_pattern(start_account)
        else:  # line pattern
            line_length = random.randint(5, 10)
            new_transactions = generate_line_pattern(start_account, line_length)
        
        transactions.extend(new_transactions)

        # For each account in the new pattern, try to start a new nested pattern
        for _, next_account in new_transactions:
            transactions.extend(generate_nested_patterns(next_account, max_depth, depth + 1))
    else:
        # If no pattern is initiated, create a normal transaction
        normal_account = generate_hash()
        transactions.append((start_account, normal_account))

    return transactions

def generate_transactions(num_accounts=100, max_depth=3):
    """Generate transactions with nested patterns and record all accounts in a table."""
    accounts = [generate_hash() for _ in range(num_accounts)]
    all_transactions = []
    long_chains = []
    sybyl_accounts_count = 0

    for account in accounts:
        transactions = generate_nested_patterns(account, max_depth)
        all_transactions.extend(transactions)
        
        # Check if the chain has more than 20 transactions
        if len(transactions) > 15:
            long_chains.append(transactions)
            sybyl_accounts_count += utils.get_unique_accounts(transactions)

    # Record all transactions in a table
    df = pd.DataFrame(all_transactions, columns=["from", "to"])
    return df, long_chains, sybyl_accounts_count

def plot_chains(transactions):
    """Plot all transactions with varying curvature to reduce overlap."""
    G = nx.DiGraph()
    G.add_edges_from(transactions)
    plt.figure(figsize=(12, 12))

    # Layout positions
    pos = nx.spring_layout(G, seed=42, k=0.3, scale=2)  # Use spring layout with adjustments

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color="skyblue")

    # Draw edges with different curvatures for each
    for edge in G.edges():
        rad = random.uniform(0.1, 0.3)  # Random curvature between 0.1 and 0.3
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[edge],
            edge_color="gray",
            alpha=0.6,
            connectionstyle=f"arc3,rad={rad}"
        )

    plt.show()

# Parameters
num_accounts = 10  # Define the total number of accounts for initial generation
max_depth = 3  # Maximum depth for nested patterns

# Generate transactions and extract long chains
df, long_chains, sybyl_accounts_count = generate_transactions(num_accounts=num_accounts, max_depth=max_depth)

#Get the total accounts count
total_accounts_count = utils.get_unique_accounts([tuple(x) for x in df.to_numpy()])

# Display the total number of chains with more than 20 transactions
print("Total number of chains with length > 20:", len(long_chains))
print("Total number of sybil accounts: ", sybyl_accounts_count)
print("Total number of accounts: ", total_accounts_count)

# Plot the long chains
# Flatten all long chains into one list of transactions for plotting
all_long_chain_transactions = [trx for chain in long_chains for trx in chain]
plot_chains(all_long_chain_transactions)

# Save the DataFrame containing all transactions to CSV in the 'data' folder
output_dir = "data"
csv_path = os.path.join(output_dir, "transactions.csv")
df.to_csv(csv_path, index=False)
print(f"Transactions saved to {csv_path}")