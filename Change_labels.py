import os
import pandas as pd
from datasets import load_dataset

print("--- Starting Multi-Label Preparation Script ---")

# --- Step 1: Define paths ---
input_csv_directory = "20_newsgroups_csv_export"
train_file = os.path.join(input_csv_directory, "train.csv")
test_file = os.path.join(input_csv_directory, "test.csv")

print(f"Attempting to load data from: '{input_csv_directory}'")

# --- Step 2: Load the dataset from local CSVs ---
try:
    ds = load_dataset("csv", data_files={"train": train_file, "test": test_file})
    print("✅ Successfully loaded dataset from local CSVs.")
except FileNotFoundError:
    print(f"\n❌ ERROR: Input files not found in '{input_csv_directory}'.")
    exit()

# --- Step 3: Define Mappings for BOTH tasks ---

# Mapping for Subject (Head 1)
subject_label_mapping = {
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

# NEW: Function to get synthetic category (Head 2)
def get_synthetic_category(original_label):
    if original_label.startswith('sci.') or original_label.startswith('comp.'):
        return 'Technical Report'
    elif original_label.startswith('talk.'):
        return 'Opinion Piece'
    elif original_label.startswith('rec.') or original_label.startswith('alt.'):
        return 'Forum Post'
    else:
        return 'Article'

# --- Step 4: Apply a combined mapping function ---
def apply_all_mappings(examples):
    original_labels = examples['label_text']
    
    # Create Subject labels
    subject_labels = [subject_label_mapping.get(label, 'Miscellaneous') for label in original_labels]
    
    # Create Category labels
    category_labels = [get_synthetic_category(label) for label in original_labels]
    
    # Add the new columns to the dataset
    examples['subject_label'] = subject_labels
    examples['category_label'] = category_labels
    return examples

print("Applying multi-task mappings...")
modified_ds = ds.map(apply_all_mappings, batched=True)

# --- Step 5: Remove the original label columns ---
print("Removing original label columns...")
final_ds = modified_ds.remove_columns(["label", "label_text"])

print("\nTransformation complete. Final multi-task dataset structure:")
print(final_ds)


# --- Step 6: Save the final dataset ---
print("\n--- Saving the processed data ---")
output_csv_directory = "20_newsgroups_processed" # Saving to a NEW folder is safer
os.makedirs(output_csv_directory, exist_ok=True)

for split, dataset in final_ds.items():
    output_path = os.path.join(output_csv_directory, f"{split}.csv")
    dataset.to_csv(output_path, index=False)
    print(f"Saved '{split}' split to '{output_path}'")

print(f"\n✅ Successfully saved final multi-task dataset to '{output_csv_directory}' folder.")
print("\n--- Script Finished ---")