import re
import csv



for i in range (0, 9):

    # Path to your TypeScript file
    input_file = f"blacklist_{i}.ts"
    # Path to your output CSV file
    output_file = f"blacklist_{i}.csv"

    # Regex pattern to match Ethereum addresses (hashes)
    hash_pattern = r"'(0x[0-9a-fA-F]{40})'"

    # List to store extracted hashes
    hashes = []

    # Open and read the TypeScript file
    with open(input_file, 'r') as file:
        for line in file:
            # Find all Ethereum addresses in the line
            match = re.findall(hash_pattern, line)
            if match:
                # Append each found hash to the list
                hashes.extend(match)

    # Write the hashes to a CSV file
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write each hash into a new row in the CSV
        for hash_value in hashes:
            writer.writerow([hash_value])

    print(f"Hashes extracted and saved to {output_file}")

    import pandas as pd

import glob

# Specify file path and pattern
file_pattern = 'blacklist_[0-9].csv'

# Get list of files
files = glob.glob(file_pattern)

# Initialize empty DataFrame
blacklist_extended = pd.DataFrame()

# Iterate through files and concatenate
for file in files:
    df = pd.read_csv(file, header=None)  # No column header
    blacklist_extended = pd.concat([blacklist_extended, df])

# Save extended blacklist to new CSV
blacklist_extended.to_csv('blacklist.csv', index=False, header=False)