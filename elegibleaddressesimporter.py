import pandas as pd

addresses = [line.strip() for line in open('eligibleAddresses.txt', 'r')]
df = pd.DataFrame({'address': addresses})
df.to_csv('data/final_elegible_accounts.csv', index=False)