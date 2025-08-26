import os
from datasets import load_dataset
import pandas as pd

# 1. Define the path where you want to save the CSV files
csv_save_directory = "./20_newsgroups_csv_export"

# 2. Create the directory if it doesn't already exist
# The exist_ok=True argument prevents an error if the folder is already there.
os.makedirs(csv_save_directory, exist_ok=True)

print(f"Directory '{csv_save_directory}' prepared.")
print("-" * 30)

# 3. Load the dataset from the Hugging Face Hub
print("Downloading and loading the 'SetFit/20_newsgroups' dataset...")
try:
    ds = load_dataset("SetFit/20_newsgroups")
    print("Dataset loaded successfully.")
    print(ds)
    print("-" * 30)

    # 4. Iterate through each split in the dataset and save it as a CSV file
    for split_name, dataset_split in ds.items():
        print(f"Processing the '{split_name}' split...")
        
        # Define the full path for the output CSV file
        output_file_path = os.path.join(csv_save_directory, f"{split_name}.csv")
        
        # Use the .to_csv() method to save the data
        dataset_split.to_csv(output_file_path)
        
        print(f"✅ Successfully saved '{split_name}' split to: {output_file_path}")

    print("-" * 30)
    print("All splits have been saved.")

    # (Optional) 5. Verify by loading one of the CSVs with pandas
    print("\nVerifying the 'train.csv' file...")
    train_df = pd.read_csv(os.path.join(csv_save_directory, "train.csv"))
    print("First 5 rows of train.csv:")
    print(train_df.head())

except Exception as e:
    print(f"An error occurred: {e}")