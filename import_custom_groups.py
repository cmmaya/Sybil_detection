import re
import pandas as pd

# Step 1: Read the customGroups.ts file
with open('customGroups.ts', 'r') as file:
    content = file.read()

# Step 2: Use regex to find all addresses inside `addresses` lists
# This regex pattern captures addresses inside 'addresses: [...]' blocks
address_pattern = r"addresses:\s*\[([^\]]*)\]"
addresses = []

# Find all matches for the address pattern
matches = re.findall(address_pattern, content, re.MULTILINE | re.DOTALL)

for match in matches:
    # Extract individual addresses from each match
    individual_addresses = re.findall(r"'(0x[a-fA-F0-9]+)'", match)
    addresses.extend(individual_addresses)

# Step 3: Create a DataFrame and export to CSV
df = pd.DataFrame(addresses, columns=["address"])
df.to_csv('addresses.csv', index=False)

print("Addresses have been successfully extracted to addresses.csv")
