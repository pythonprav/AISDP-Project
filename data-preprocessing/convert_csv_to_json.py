import pandas as pd
import json

# Path to your wine dataset
csv_file = "data/wine_quality_assignment.csv"

# Read the CSV file
df = pd.read_csv(csv_file)

# Convert DataFrame to JSON
data_json = df.to_dict(orient='records')

# Save JSON to a file (optional, for testing purposes)
with open("data/wine_quality.json", "w") as json_file:
    json.dump(data_json, json_file, indent=4)

print("CSV has been converted to JSON!")