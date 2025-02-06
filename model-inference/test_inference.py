import requests
import json

# Define API endpoint
url = "http://127.0.0.1:5000/predict-wine-quality"

# Define a sample wine input (Make sure these match `feature_names.csv`)
sample_data = {
    "fixed_acidity": 6.2,
    "volatile_acidity": 0.73,
    "citric_acid": 0.03,
    "residual_sugar": 1.6,
    "chlorides": 0.0755,
    "free_sulfur_dioxide": 5,
    "total_sulfur_dioxide": 12,
    "density": 0.0946,
    "pH": 3.65,
    "sulphates": 0.69,
    "alcohol": 9.25,
    "color": 1  
}

# Send request
response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(sample_data))

# Print response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())