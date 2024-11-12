import pandas as pd
import glob

def process_csv_files(folder_path):
    """
    Reads CSV files from a folder with filenames starting from ethereum_batch_0.csv to ethereum_batch_9.csv,
    appends them in order, and removes the "\" character from the "from" and "to" columns.

    Args:
        folder_path (str): Path to the folder containing CSV files.

    Returns:
        None
    """

    # Define the pattern for filenames
    filename_pattern = "xdai_batch_[0-10].csv"

    # Use glob to find files matching the pattern in the specified folder
    file_paths = glob.glob(f"{folder_path}/*" + filename_pattern)

    # Initialize an empty list to store DataFrames
    dfs = []

    # Iterate over each file path and read the CSV file
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)
            # Remove the "\" character from the "from" and "to" columns
            df['from'] = df['from'].str.replace('\\', '')
            df['to'] = df['to'].str.replace('\\', '')
            dfs.append(df)
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")

    # Concatenate the DataFrames
    concatenated_df = pd.concat(dfs, ignore_index=True)

    # Save the concatenated DataFrame to a new CSV file
    concatenated_df.to_csv(f"{folder_path}/xdai_batch.csv", index=False)


# Example usage:
folder_path = "data"
process_csv_files(folder_path)

print("Files processed and saved as xdai_batch.csv")