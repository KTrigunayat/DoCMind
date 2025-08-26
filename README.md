# DocMind: PDF Parser & Text Classification Pipeline

This project contains two primary components:
1.  A **PDF Parsing API** built with FastAPI to extract text from uploaded PDF files.
2.  A **Data Processing Pipeline** to download and transform the 20 Newsgroups dataset for multi-label text classification.

## File Structure

```
.
├── 20_newsgroups_csv_export/   # Raw data from Hugging Face
│   ├── train.csv
│   └── test.csv
├── 20_newsgroups_processed/    # Final, processed data
│   ├── train.csv
│   └── test.csv
├── main.py                     # FastAPI application for PDF parsing
├── Dataset.py                  # Script to download the raw dataset
├── Change_labels.py            # Script to process and remap labels
└── README.md                   # This documentation
```

---

## 1. PDF Parsing API

The `main.py` script launches a web server with an endpoint for parsing PDF files.

### Dependencies

- fastapi
- uvicorn
- python-multipart
- PyMuPDF

Install them using pip:
```bash
pip install fastapi uvicorn python-multipart PyMuPDF
```

### How to Run

1.  Navigate to the project directory in your terminal.
2.  Run the application using `uvicorn`:

    ```bash
    uvicorn main:app --reload
    ```

3.  The API will be live at `http://127.0.0.1:8000`.

### API Endpoint

- **POST** `/parse-upload/`
  - **Purpose**: Upload a PDF file to extract its text content.
  - **Request**: `multipart/form-data` with a `file` field containing the PDF.
  - **Response**: A JSON object with the filename, content type, and the extracted text.

---

## 2. 20 Newsgroups Data Pipeline

This two-step pipeline downloads the 20 Newsgroups dataset and processes it for a multi-label classification task.

### Dependencies

- pandas
- datasets

Install them using pip:
```bash
pip install pandas datasets
```

### Step 1: Download the Dataset

Run the `Dataset.py` script to download the raw data from Hugging Face and save it locally.

```bash
python Dataset.py
```

This will create the `20_newsgroups_csv_export/` directory containing the raw `train.csv` and `test.csv` files.

### Step 2: Process and Remap Labels

Run the `Change_labels.py` script to clean the data and create two new label columns for multi-label classification.

```bash
python Change_labels.py
```

This script performs the following actions:
- Reads the raw data from `20_newsgroups_csv_export/`.
- Creates a `subject_label` based on the original 20 newsgroups.
- Creates a `category_label` (e.g., `Technical Report`, `Opinion Piece`) based on the original labels.
- Removes the old labels.
- Saves the final, processed data to the `20_newsgroups_processed/` directory.

### Final Output

The processed CSV files in `20_newsgroups_processed/` contain three columns:
- `text`: The original post content.
- `subject_label`: The general subject of the post.
- `category_label`: The synthetic category of the post.
