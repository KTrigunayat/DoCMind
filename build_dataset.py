import fitz  # PyMuPDF
import os
import pandas as pd
from tqdm import tqdm # For a nice progress bar

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts all text content from a given PDF file.

    Args:
        pdf_path (str): The full path to the PDF file.

    Returns:
        str: The extracted text content. Returns an empty string if an error occurs.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return ""

def create_dataset_from_folders(root_directory: str) -> pd.DataFrame:
    """
    Walks through a hierarchical directory, extracts text from PDFs,
    and creates a labeled pandas DataFrame.

    Assumes a folder structure like:
    - root_directory/
      - Computer Science/
        - AI & ML/
          - doc1.pdf
          - doc2.pdf
        - DevOps/
          - doc3.pdf
      - Finance/
        - Accounts/
          - doc4.pdf

    Args:
        root_directory (str): The path to the main folder containing subject folders.

    Returns:
        pd.DataFrame: A DataFrame with columns ['filename', 'text', 'subject', 'sub_field'].
    """
    records = []
    
    # Check if the directory exists
    if not os.path.isdir(root_directory):
        print(f"Error: Directory not found at '{root_directory}'")
        return pd.DataFrame()

    # Create a list of all PDF files to process for the progress bar
    pdf_files_to_process = []
    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.lower().endswith(".pdf"):
                pdf_files_to_process.append(os.path.join(dirpath, filename))

    print(f"Found {len(pdf_files_to_process)} PDF files to process.")

    # Process files with a progress bar
    for pdf_path in tqdm(pdf_files_to_process, desc="Parsing PDFs"):
        # Extract labels from the path structure
        # Example path: ./data/Computer Science/AI & ML/doc1.pdf
        path_parts = os.path.normpath(pdf_path).split(os.sep)

        if len(path_parts) >= 4: # Ensure the path is deep enough
            subject = path_parts[-3]
            sub_field = path_parts[-2]
            filename = path_parts[-1]

            text = extract_text_from_pdf(pdf_path)

            if text:  # Only add record if text extraction was successful
                records.append({
                    "filename": filename,
                    "text": text,
                    "subject": subject,
                    "sub_field": sub_field
                })
        else:
            print(f"Skipping file due to unexpected path structure: {pdf_path}")

    return pd.DataFrame(records)

# --- Main execution ---
if __name__ == "__main__":
    # IMPORTANT: Replace this with the actual path to your main data folder
    # This folder should contain the "Computer Science" and "Finance" sub-folders.
    data_folder = "./Your_Training_Data" # <--- CHANGE THIS PATH

    print(f"Starting PDF processing from directory: {data_folder}")
    
    # Create the dataset
    df = create_dataset_from_folders(data_folder)

    if not df.empty:
        print("\nSuccessfully created dataset!")
        print("------------------------------")
        print("Dataset Info:")
        print(f"Total documents processed: {len(df)}")
        
        print("\nDistribution of Subjects (Level 1):")
        print(df['subject'].value_counts())
        
        print("\nDistribution of Sub-fields (Level 2):")
        print(df['sub_field'].value_counts())
        
        print("\nFirst 5 rows of the dataset:")
        print(df.head())

        # Save the final dataset to a CSV file
        output_csv_path = "training_dataset.csv"
        df.to_csv(output_csv_path, index=False)
        print(f"\nDataset saved successfully to '{output_csv_path}'")
    else:
        print("\nCould not create dataset. Please check the directory path and PDF files.")