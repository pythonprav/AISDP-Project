from flask import Flask, jsonify
import pandas as pd
import re
import json
import os
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Corrected directory paths
RAW_DATA_DIR = "data-preprocessing/raw_data"
OUTPUT_DIR = "volumes/data"
USER_INPUTS_DIR = "volumes/user"

CSV_FILE = os.path.join(RAW_DATA_DIR, "wine_quality_assignment.csv")
JSON_FILE = os.path.join(OUTPUT_DIR, "wine_quality.json")
CLEANED_CSV = os.path.join(OUTPUT_DIR, "cleaned_wine_quality.csv")


def convert_csv_to_json():
    """Convert CSV to JSON if it exists."""
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(f"CSV file not found at {CSV_FILE}.")
    
    df = pd.read_csv(CSV_FILE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure the output directory exists
    df.to_json(JSON_FILE, orient='records', indent=4)
    print(f"✅ CSV converted to JSON: {JSON_FILE}")


def clean_column(column):
    """Clean non-numeric columns."""
    return column.apply(lambda x: re.sub(r'[^\d.]', '', str(x)) if isinstance(x, str) else x)


def preprocess_data_logic(df):
    """Preprocess the dataset: clean, encode, and transform."""
    # Drop unnecessary columns
    if 'Sample' in df.columns:
        df.drop('Sample', axis=1, inplace=True)

    # Clean numeric columns
    for col in df.columns:
        if col not in ['color', 'quality']:
            df[col] = clean_column(df[col])
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remove invalid rows
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    # Encode color (white → 0, red → 1)
    if 'color' in df.columns:
        encoder = LabelEncoder()
        df['color'] = encoder.fit_transform(df['color'])

    # Remap quality to 5 categories
    if 'quality' in df.columns:
        quality_map = {3: 1, 4: 2, 5: 3, 6: 3, 7: 4, 8: 5}
        df['quality'] = df['quality'].map(quality_map)
        df.dropna(subset=['quality'], inplace=True)
        df['quality'] = df['quality'].astype(int)

    return df


@app.route('/get-data', methods=['GET', 'POST'])
def preprocess_dataset():
    """Preprocess the initial dataset and show it in the browser."""
    try:
        # Convert CSV to JSON
        convert_csv_to_json()

        # Load JSON
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)

        df = pd.DataFrame(data)

        # Preprocess
        df = preprocess_data_logic(df)

        # Save cleaned CSV
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        df.to_csv(CLEANED_CSV, index=False)

        # Convert processed DataFrame to JSON to display
        processed_json = df.to_dict(orient='records')

        return jsonify({
            "message": "Initial dataset preprocessed successfully.",
            "cleaned_data_preview": processed_json[:5],  # Show only the first 5 rows
            "total_rows": len(df),
            "cleaned_csv_path": CLEANED_CSV
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/process-user-input', methods=['POST'])
def process_user_input():
    """Preprocess user-uploaded data."""
    try:
        input_file = os.path.join(USER_INPUTS_DIR, "input.csv")
        if not os.path.exists(input_file):
            return jsonify({"error": "User input file not found."}), 400

        df = pd.read_csv(input_file)
        df = preprocess_data_logic(df)

        # Save cleaned user input
        cleaned_input_file = os.path.join(USER_INPUTS_DIR, "cleaned_input.csv")
        os.makedirs(USER_INPUTS_DIR, exist_ok=True)
        df.to_csv(cleaned_input_file, index=False)

        # Show processed data in browser
        processed_json = df.to_dict(orient='records')

        return jsonify({
            "message": "User input processed successfully.",
            "processed_data_preview": processed_json[:5],
            "total_rows": len(df),
            "cleaned_csv_path": cleaned_input_file
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)