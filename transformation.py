
import pandas as pd
import json
import re

# Define the path to the CSV file
csv_file_path = 'sample_733fa042.csv'

#  1. Read and Flatten the JSON Data 

# Read the CSV file. The data is complex, so we read it as a single column first
# and then use regex to split the ID from the JSON string.
try:
    df = pd.read_csv(csv_file_path, header=None, names=['id', 'json_data'])
except Exception:
    # Fallback for complex CSV structure
    df = pd.read_csv(csv_file_path, header=None, names=['full_line'])
    def safe_split(line):
        # Regex to split 'id,"{json_string}"'
        match = re.match(r'([a-f0-9-]+),"(.*)"', str(line))
        if match:
            return match.groups()
        return str(line), None

    df[['id', 'json_data']] = df['full_line'].apply(lambda x: pd.Series(safe_split(x)))
    df.drop(columns=['full_line'], inplace=True)

# Function to safely parse the JSON string
def parse_json_string(json_str):
    if pd.isna(json_str):
        return {}
    try:
        # Unescape the double quotes that were used to escape quotes inside the JSON string
        cleaned_str = json_str.replace('""', '"')
        return json.loads(cleaned_str)
    except json.JSONDecodeError as e:
        # print(f"Error decoding JSON: {e} for string: {json_str[:50]}...")
        return {}
    except AttributeError:
        return {}

# Apply the parsing function and flatten the JSON data
json_data = df['json_data'].apply(parse_json_string)
df_flattened = pd.json_normalize(json_data)
df_final = pd.concat([df['id'], df_flattened], axis=1)

#  2. Data Type Correction 

# Define the desired data types
dtype_map = {
    'active': 'bool',
    'adminFee': 'int64',
    'basePrice': 'int64',
    'problem': 'bool',
    'status': 'bool',
    'userAdminFee': 'int64',
    'userSellPrice': 'int64',
    'version': 'int64'
}

# Apply type conversion
for col, dtype in dtype_map.items():
    if col in df_final.columns:
        if dtype == 'bool':
            # Convert to boolean, handling various representations (True/False, 1/0)
            df_final[col] = df_final[col].astype(str).str.lower().map({'true': True, 'false': False, '1': True, '0': False}).fillna(False).astype('bool')
        else:
            # Convert to numeric, coercing errors to NaN, filling NaN with 0, then converting to target type
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce').fillna(0).astype(dtype)

# Convert 'createdAt' to datetime
if 'createdAt' in df_final.columns:
    df_final['createdAt'] = pd.to_datetime(df_final['createdAt'], errors='coerce')

#  3. Display the final dtypes 
print(df_final.dtypes.to_markdown(numalign="left", stralign="left"))
