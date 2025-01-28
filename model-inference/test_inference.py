import requests
import pandas as pd

# Test input data
test_data = {
    "fixed_acidity": [7.4, 7.8],
    "volatile_acidity": [0.7, 0.88],
    "citric_acid": [0.0, 0.0],
    "residual_sugar": [1.9, 2.6],
    "chlorides": [0.076, 0.098],
    "free_sulfur_dioxide": [11.0, 25.0],
    "total_sulfur_dioxide": [34.0, 67.0],
    "density": [0.9978, 0.9968],
    "pH": [3.51, 3.2],
    "sulphates": [0.56, 0.68],
    "alcohol": [9.4, 9.8],
    "color": [1, 1]  # Assuming 1 for red
}

# API endpoint
url = "http://127.0.0.1:5000/predict"

# Send the POST request
response = requests.post(url, json=pd.DataFrame(test_data).to_dict(orient="records"))

# Print the response
if response.status_code == 200:
    print("Predictions:", response.json()["predictions"])
else:
    print("Error:", response.json())