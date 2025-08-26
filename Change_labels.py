import os
import random
from datasets import load_dataset

print("--- Starting Change_labels.py Script ---")

# --- Step 1: Define the path to your INPUT CSV files ---
input_csv_directory = "20_newsgroups_csv_export" #<-- UPDATE if your folder is named differently
train_file = os.path.join(input_csv_directory, "train.csv")
test_file = os.path.join(input_csv_directory, "test.csv")

print(f"Attempting to load data from: '{input_csv_directory}'")

# --- Step 2: Load the dataset from the local CSV files ---
try:
    ds = load_dataset("csv", data_files={"train": train_file, "test": test_file})
    print("✅ Successfully loaded dataset from local CSVs.")
except FileNotFoundError:
    print(f"\n❌ ERROR: Input files not found in '{input_csv_directory}'.")
    print("Please ensure the folder name in the script matches your actual folder name.")
    exit()

# --- Step 3: Define the mapping to broader categories ---
label_mapping = {
    'comp.graphics': 'Computer Technology', 'comp.os.ms-windows.misc': 'Computer Technology',
    'comp.sys.ibm.pc.hardware': 'Computer Technology', 'comp.sys.mac.hardware': 'Computer Technology',
    'comp.windows.x': 'Computer Technology', 'rec.autos': 'Recreation & Sport',
    'rec.motorcycles': 'Recreation & Sport', 'rec.sport.baseball': 'Recreation & Sport',
    'rec.sport.hockey': 'Recreation & Sport', 'sci.crypt': 'Science',
    'sci.electronics': 'Science', 'sci.med': 'Science', 'sci.space': 'Science',
    'misc.forsale': 'Miscellaneous', 'talk.politics.misc': 'Politics',
    'talk.politics.guns': 'Politics', 'talk.politics.mideast': 'Politics',
    'soc.religion.christian': 'Religion', 'talk.religion.misc': 'Religion',
    'alt.atheism': 'Religion'
}

# --- Step 4: Apply the mapping function ---
def remap_labels(examples):
    new_labels = [label_mapping.get(label, 'Miscellaneous') for label in examples['label_text']]
    examples['label_text'] = new_labels
    return examples

print("Remapping labels...")
modified_ds = ds.map(remap_labels, batched=True)

# --- Step 5: Remove the 'label' column ---
print("Removing old 'label' column...")
final_ds = modified_ds.remove_columns("label")

print("\nTransformation complete. Final dataset structure:")
print(final_ds)


# --- Step 6: SAVE THE MODIFIED DATASET ---
print("\n--- Saving the processed data ---")

# --- CHOOSE ONE SAVING METHOD BELOW ---

# Option 1: Save as new CSV files (Recommended for you)
# This will create a new folder and save train.csv and test.csv inside it.
output_csv_directory = "20_newsgroups_csv_export"
os.makedirs(output_csv_directory, exist_ok=True) # Create folder if it doesn't exist

for split, dataset in final_ds.items():
    output_path = os.path.join(output_csv_directory, f"{split}.csv")
    dataset.to_csv(output_path)
    print(f"Saved '{split}' split to '{output_path}'")

print(f"\n✅ Successfully saved modified dataset to '{output_csv_directory}' folder.")


# # Option 2: Save in native Arrow format (Faster for re-loading in 'datasets')
# # Uncomment the lines below and comment out Option 1 if you prefer this.
# output_arrow_directory = "20_newsgroups_modified_arrow"
# final_ds.save_to_disk(output_arrow_directory)
# print(f"\n✅ Successfully saved modified dataset to '{output_arrow_directory}' folder.")

print("\n--- Script Finished ---")