from flask import Flask, jsonify, request
import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder
import os

app = Flask(__name__)

def clean_column(column):
    """
    Clean non-numeric values in a column by removing invalid characters.
    """
    return column.apply(lambda x: re.sub(r'[^\d\.]', '', str(x)) if isinstance(x, str) else x)

def preprocess_data_logic(df):
    """
    Perform data cleaning and preprocessing on the DataFrame.
    """
    # Drop unwanted column 'Sample' if it exists
    if 'Sample' in df.columns:
        df.drop(columns=['Sample'], inplace=True)

    # Clean numeric columns
    for col in df.columns:
        if col not in ['color', 'quality']:  # Exclude categorical/target columns
            df[col] = clean_column(df[col])  # Remove non-numeric characters
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric

    # Handle missing values
    df.dropna(inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Remove rows where 'quality' equals 2
    if 'quality' in df.columns:
        df = df[df['quality'] != 2].copy()  # Explicitly create a copy

    # Encode 'color' column if it exists
    if 'color' in df.columns:
        encoder = LabelEncoder()
        df.loc[:, 'color'] = encoder.fit_transform(df['color'])  # Use .loc for modification

    # Map 'quality' values to star ratings if it exists
    if 'quality' in df.columns:
        quality_map = {
            1: '1 Star', 2: '1 Star',
            3: '2 Star', 4: '2 Star',
            5: '3 Star', 6: '3 Star',
            7: '4 Star', 8: '4 Star',
            9: '5 Star', 10: '5 Star'
        }
        star_encoding = {
            '1 Star': 1,
            '2 Star': 2,
            '3 Star': 3,
            '4 Star': 4,
            '5 Star': 5
        }
        # Perform the two mappings in a single step to avoid intermediate type conflicts
        df.loc[:, 'quality'] = df['quality'].map(quality_map).map(star_encoding).astype(int)

    return df

@app.route('/get-data', methods=['POST'])
def preprocess_data():
    """
    Flask route to preprocess incoming JSON or CSV data.
    """
    try:
        # Ensure the data directory exists
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)

        # Check if request contains a CSV file
        if 'file' in request.files:
            csv_file = request.files['file']
            df = pd.read_csv(csv_file)  # Read CSV file
        else:
            # Assume JSON input if no CSV file is provided
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data received"}), 400
            df = pd.DataFrame(data)

        # Convert CSV to JSON before preprocessing (if CSV was provided)
        json_filepath = os.path.join(data_dir, "wine_quality.json")
        df.to_json(json_filepath, orient="records", indent=4)

        # Apply preprocessing logic
        df = preprocess_data_logic(df)

        # Define output file path
        cleaned_csv_filepath = os.path.join(data_dir, "cleaned_wine_quality.csv")

        # Save the cleaned data
        df.to_csv(cleaned_csv_filepath, index=False)

        return jsonify({
            "message": f"Data preprocessed successfully! Cleaned file saved to {cleaned_csv_filepath}",
            "json_saved_to": json_filepath
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
