import requests
import json

# URL of your running Flask app
url = "http://127.0.0.1:5000/get-data"

# Path to your JSON file
json_file_path = "data/wine_quality.json"

# Read the JSON data
with open(json_file_path, "r") as file:
    json_data = json.load(file)

# Send a POST request to the Flask endpoint
response = requests.post(url, json=json_data)

# Print the response from the Flask server
print("Status Code:", response.status_code)
print("Response JSON:", response.json())