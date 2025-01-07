# Web Application (winequality_app.py)
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        # Process login (this can include user authentication logic)
        username = request.form['username']
        password = request.form['password']
        # Mock authentication check
        if username == "user" and password == "password":
            return render_template('dashboard.html')
        else:
            return "Login Failed!"
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Collect feature inputs from user
    input_features = {
        "feature1": request.form['feature1'],
        "feature2": request.form['feature2'],
        # Add more features as required
    }

    # Send data to the inference container
    response = requests.post('http://model-inference:5002/predict', json=input_features)
    result = response.json()

    return render_template('dashboard.html', prediction=result["prediction"], probability=result["probability"])
#main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
