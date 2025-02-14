import os
from flask import Flask, render_template, request
import pandas as pd
import time

# Define paths to Persistent Volumes (PVs)
USER_DIR = "/mnt/user"  # Path where Web App saves user data


# Load trained model
model_file = os.path.join(USER_DIR, "trained_model.pkl")

# Ensure directories exist
os.makedirs(USER_DIR, exist_ok=True)

app = Flask(__name__)

@app.route("/")
def index():
    """Render the home page (index.html)."""
    return render_template("index.html")

@app.route("/model_pred_csv", methods=["GET", "POST"])
def model_pred_csv():
    if request.method == "POST":
        # Save CSV to `userinputs` PV for processing
        csv_file = request.files["csvFile"]
        if csv_file:
            file_path = os.path.join(USER_DIR, "input.csv")
            csv_file.save(file_path)
            
            # Wait for the processed result from Model Inference
            output_file = os.path.join(USER_DIR, "predictions.csv")
            for _ in range(10):  # Wait for max ~10s
                if os.path.exists(output_file):
                    df = pd.read_csv(output_file)
                    return render_template("model_pred_csv.html", tables=df.to_html())
                time.sleep(1)
            
            return "Processing took too long. Try again later."

    return render_template("model_pred_csv.html")

@app.route("/model_pred_manual", methods=["GET", "POST"])
def model_pred_manual():
    if request.method == "POST":
        # Collect input values from the form
        data = {
            "fixed_acidity": float(request.form.get("fixed_acidity")),
            "volatile_acidity": float(request.form.get("volatile_acidity")),
            "citric_acid": float(request.form.get("citric_acid")),
            "residual_sugar": float(request.form.get("residual_sugar")),
            "chlorides": float(request.form.get("chlorides")),
            "free_sulfur_dioxide": float(request.form.get("free_sulfur_dioxide")),
            "total_sulfur_dioxide": float(request.form.get("total_sulfur_dioxide")),
            "density": float(request.form.get("density")),
            "pH": float(request.form.get("pH")),
            "sulphates": float(request.form.get("sulphates")),
            "alcohol": float(request.form.get("alcohol")),
            "color": request.form.get("color")
        }

        # Convert data to DataFrame and save to `userinputs` PV
        df = pd.DataFrame([data])
        input_file = os.path.join(USER_DIR, "input.csv")
        df.to_csv(input_file, index=False)

        # Wait for the processed result from Model Inference
        output_file = os.path.join(USER_DIR, "predictions.csv")
        for _ in range(10):  # Wait for max ~10s
            if os.path.exists(output_file):
                with open(output_file, "r") as f:
                    prediction = f.read().strip()
                return render_template("model_pred_manual.html", prediction=prediction)
            time.sleep(1)

        return "Processing took too long. Try again later."

    return render_template("model_pred_manual.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)