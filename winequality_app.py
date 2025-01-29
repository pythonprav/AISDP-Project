from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import joblib  # or pickle, if you saved your model that way

app = Flask(__name__)

# (Optional) Load your pre-trained model at startup
model = joblib.load("my_wine_model.joblib")

@app.route("/")
def index():
    # Render the home page (index.html)
    return render_template("index.html")

@app.route("/model_pred_csv", methods=["GET", "POST"])
def model_pred_csv():
    if request.method == "POST":
        # The user uploaded a CSV, handle it:
        csv_file = request.files["csvFile"]
        if csv_file:
            df = pd.read_csv(csv_file)  # read CSV as DataFrame
            # Predict with your model (assuming it expects columns consistent with your dataset)
            predictions = model.predict(df.drop("quality", axis=1, errors="ignore"))
            
            # Or do some logic to combine predictions with the DataFrame
            df["prediction"] = predictions
            
            # Return the same page but with results:
            return render_template("model_pred_csv.html", tables=df.to_html())
    # If GET, just show the form
    return render_template("model_pred_csv.html")

@app.route("/model_pred_manual", methods=["GET", "POST"])
def model_pred_manual():
    if request.method == "POST":
        # Grab form data
        fixed_acid = float(request.form.get("fixed_acid"))
        volatile_acid = float(request.form.get("volatile_acid"))
        citric_acid   = float(request.form.get("citric_acid"))
        # etc. for all features...
        color         = request.form.get("color")  # "red" or "white", if used
        
        # Put features in a list or dataframe row
        X = pd.DataFrame([{
            "fixed_acidity": fixed_acid,
            "volatile_acidity": volatile_acid,
            "citric_acid": citric_acid,
            # ...
        }])
        
        # Predict
        prediction = model.predict(X)[0]
        
        # Return the same page but show the prediction
        return render_template("model_pred_manual.html", prediction=prediction)

    # If GET, just show the form
    return render_template("model_pred_manual.html")

if __name__ == "__main__":
    app.run(debug=True)
