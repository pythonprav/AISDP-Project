from flask import Flask, jsonify, request
import pandas as pd
import re
import json
import os
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Directory Paths (adjust for Docker)
RAW_DATA_FOLDER = "data-preprocessing/raw_data"   # For local runs
DATA_FOLDER = "volumes/data"
USER_INPUTS_DIR = "volumes/user"


def convert_csv_to_json():
    """
    Converts wine_quality_assignment.csv to JSON and saves it in the volumes/data folder.
    """
    csv_file = os.path.join(RAW_DATA_FOLDER, "wine_quality_assignment.csv")
    json_file = os.path.join(DATA_FOLDER, "wine_quality.json")

    # Ensure the data folder exists
    os.makedirs(DATA_FOLDER, exist_ok=True)

    # Check if the CSV file exists
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found at {csv_file}. Ensure it exists in '{RAW_DATA_FOLDER}'.")

    # Read CSV and convert to JSON
    df = pd.read_csv(csv_file)
    df.to_json(json_file, orient='records', indent=4)

    print(f"CSV has been converted to JSON and saved to {json_file}")
    return json_file


def clean_column(column):
    """
    Clean non-numeric values in a column by removing invalid characters.
    """
    return column.apply(lambda x: re.sub(r'[^\d\.]', '', str(x)) if isinstance(x, str) else x)


def preprocess_data_logic(df):
    """
    Perform data cleaning and preprocessing on the DataFrame.
    """
    # Remove unnecessary columns if present
    if 'Sample' in df.columns:
        df.drop(columns=['Sample'], inplace=True)

    # Clean numeric columns
    for col in df.columns:
        if col not in ['color', 'quality']:
            df[col] = clean_column(df[col])
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Handle missing and duplicate values
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    # Remove invalid quality values
    if 'quality' in df.columns:
        df = df[df['quality'] != 2].copy()

    # Encode 'color' if present
    if 'color' in df.columns:
        encoder = LabelEncoder()
        df['color'] = encoder.fit_transform(df['color'])

    # Map quality scores to grouped categories
    if 'quality' in df.columns:
        quality_map = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5, 10: 5}
        df['quality'] = df['quality'].map(quality_map).astype(int)

    return df


@app.route('/get-data', methods=['POST'])
def preprocess_data():
    """
    Flask route to preprocess JSON data.
    """
    try:
        # Step 1: Read the JSON file
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Step 2: Convert JSON data to DataFrame
        df = pd.DataFrame(data)

        # Step 3: Apply preprocessing logic
        df = preprocess_data_logic(df)

        # Step 4: Save the cleaned dataset to CSV
        cleaned_csv = os.path.join(DATA_FOLDER, "cleaned_wine_quality.csv")
        df.to_csv(cleaned_csv, index=False)

        return jsonify({
            "message": f"Data preprocessed successfully! Cleaned file saved to {cleaned_csv}"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def process_user_input():
    """
    Flask route to preprocess user-uploaded input data dynamically.
    """
    try:
        input_file = os.path.join(USER_INPUTS_DIR, "input.csv")
        if not os.path.exists(input_file):
            return jsonify({"error": "No input file found"}), 400

        # Read and clean user input
        df = pd.read_csv(input_file)
        df = preprocess_data_logic(df)

        # Save cleaned user input for inference
        cleaned_input_file = os.path.join(USER_INPUTS_DIR, "cleaned_input.csv")
        df.to_csv(cleaned_input_file, index=False)

        return jsonify({"message": f"User input processed and saved to {cleaned_input_file}"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run on Startup: Automatically generate cleaned CSV
json_file_path = convert_csv_to_json()
with open(json_file_path, "r") as file:
    data = json.load(file)

# Apply preprocessing to create cleaned_wine_quality.csv
df = pd.DataFrame(data)
df = preprocess_data_logic(df)
cleaned_csv = os.path.join(DATA_FOLDER, "cleaned_wine_quality.csv")
df.to_csv(cleaned_csv, index=False)
print(f"Cleaned CSV created at {cleaned_csv}")

# Run Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)