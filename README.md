# Data Transformation Script: JSON Flattening and Type Correction

## Project Description

This repository contains a Python script designed to solve a common data engineering task: **flattening a nested JSON column within a CSV file and ensuring correct data type assignment** for the resulting columns.

The script was developed as part of the Fazz Data Engineer Test (Task 2) and is specifically tailored to process the `sample_733fa042.csv` file.

## Prerequisites

The script requires Python 3.x and the following libraries:

*   **pandas**: For data manipulation and DataFrame operations.
*   **json**: For parsing the JSON strings.
*   **re**: For regular expression operations used in safely splitting the complex CSV format.

Install the required libraries using `pip` command:

```bash
pip install pandas
pip install tabulate
```

## File Structure

The repository should contain the following files:

```
.
├── transformation.py
└── sample_733fa042.csv  # The input data file
└── README.md
```

## Usage

1.  Ensure the input file (`sample_733fa042.csv`) is in the same directory as the script, or update the `csv_file_path` variable in the script to point to the correct location.
2.  Run the script from your terminal:

```bash
python3 transformation.py
```

The script will print the final DataFrame's column names and their corrected data types to the console.

## Script Functionality (`transformation.py`)

The script performs the following key steps:

1.  **Safe CSV Reading**: It handles the complex CSV structure where the JSON string contains escaped quotes (`""`) and is enclosed in quotes, which can confuse standard CSV parsers. It uses a regex-based approach to reliably separate the primary ID column from the JSON data column.
2.  **JSON Flattening**: It uses a custom `parse_json_string` function to unescape the quotes within the JSON string and then utilizes `pandas.json_normalize` to expand all key-value pairs from the JSON into new, separate columns in the DataFrame.
3.  **Data Type Correction**: It explicitly casts the new columns to their appropriate data types based on the data's nature (e.g., `active` to `bool`, `basePrice` to `int64`, `createdAt` to `datetime64[ns]`). This ensures the data is ready for downstream analytical processing.

### Corrected Data Types

The final output of the script is a table showing the corrected data types for the flattened DataFrame:

| Column | Data Type |
| :--- | :--- |
| id | object |
| active | bool |
| adminFee | int64 |
| basePrice | int64 |
| code | object |
| createdAt | datetime64[ns] |
| description | object |
| id | object |
| name | object |
| operatorCode | object |
| partnerId | object |
| problem | bool |
| status | bool |
| type | object |
| userAdminFee | int64 |
| userSellPrice | int64 |
| version | int64 |
| updatedAt | object |
| isIgnored | object |

*Note: The `id` column appears twice because the original CSV had an ID column, and the flattened JSON also contained an `id` field. Both are retained as `object` (string) type.*
