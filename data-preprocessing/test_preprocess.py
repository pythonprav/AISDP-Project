import requests
import json

# Load the JSON data
with open("data/wine_quality.json", "r") as json_file:
    data = json.load(json_file)

# Send POST request to the API
response = requests.post("http://127.0.0.1:5000/get-data", json=data)

# Print the API's response
print(response.json())