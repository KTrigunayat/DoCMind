# 20 Newsgroups Dataset Processing Pipeline

This project provides a simple, two-step pipeline to download, process, and clean the **20 Newsgroups dataset**. The primary goal is to re-categorize the 20 fine-grained newsgroup labels into 6 broader subject categories, making the dataset suitable for more general text classification tasks.

## File Structure

The complete project structure, after running all scripts, will look like this:

```
.
├── 20_newsgroups_csv/         # Directory for cleaned and processed data after downloaded from Hugging Face
│   ├── train.csv
│   └── test.csv
└── README.md                  # This documentation
```

## 1. 20 Newsgroups Dataset Processing

```bash
python Dataset.py
```
After this step is complete, you will have the `20_newsgroups_csv/` folder containing the raw `train.csv` and `test.csv` files.

### Step 2: Clean and Remap the Labels

Next, run the `Change_labels.py` script. This script reads the raw CSV files, performs the label modifications, and saves the cleaned data into a new directory.

```bash
python Change_labels.py
```
This script will create the `20_newsgroups_modified_csv/` directory containing the final, processed versions of `train.csv` and `test.csv`.

## Script Descriptions

### `Dataset.py`
- **Purpose**: To acquire the initial data.
- **Actions**:
  1. Downloads the `SetFit/20_newsgroups` dataset using the `datasets` library.
  2. Saves each split (`train` and `test`) as a separate CSV file.
  3. Places the output files in the `./20_newsgroups_csv/` directory.

### `Change_labels.py`
- **Purpose**: To clean and transform the raw data for analysis.
- **Actions**:
  1. Loads the `train.csv` and `test.csv` files from the `20_newsgroups_csv/` directory.
  2. **Remaps Labels**: Converts the 20 specific newsgroup labels into 6 broader categories:
     - `Computer Technology`
     - `Science`
     - `Politics`
     - `Religion`
     - `Recreation & Sport`
     - `Miscellaneous`
  3. **Cleans Columns**: Removes the original numeric `label` column, keeping only the `text` and the new `label_text` columns.
  4. Saves the modified `train` and `test` datasets as new CSV files in the `./20_newsgroups_modified_csv/` directory.

## Final Output

The final, analysis-ready data is located in the `20_newsgroups_modified_csv/` directory. These CSV files contain two columns:
- `text`: The full text content of the newsgroup post.
- `label_text`: The new, broader category label for the post.
