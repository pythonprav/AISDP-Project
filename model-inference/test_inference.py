import requests
import json

# Define the endpoint
url = "http://127.0.0.1:5000/predict"

# Define sample input data (make sure it matches feature names)
sample_data = [
    {
        "fixed_acidity": 7.4,
        "volatile_acidity": 0.7,
        "citric_acid": 0,
        "residual_sugar": 1.9,
        "chlorides": 0.076,
        "free_sulfur_dioxide": 11,
        "total_sulfur_dioxide": 34,
        "density": 0.9978,
        "pH": 3.51,
        "sulphates": 0.56,
        "alcohol": 9.4,
        "color": 1
    }
]

# Send the POST request
response = requests.post(url, json=sample_data)

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())