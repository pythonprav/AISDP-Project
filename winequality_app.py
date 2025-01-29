from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import joblib  

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
        fixed_acidity = float(request.form.get("fixed_acidity"))
        volatile_acidity = float(request.form.get("volatile_acidity"))
        citric_acid = float(request.form.get("citric_acid"))
        residual_sugar = float(request.form.get("residual_sugar"))
        chlorides = float(request.form.get("chlorides"))
        free_sulfur_dioxide = float(request.form.get("free_sulfur_dioxide"))
        total_sulfur_dioxide = float(request.form.get("total_sulfur_dioxide"))
        density = float(request.form.get("density"))
        pH = float(request.form.get("pH"))  # Include pH
        sulphates = float(request.form.get("sulphates"))
        alcohol = float(request.form.get("alcohol"))
        color = request.form.get("color")  # "red" or "white"

        # Put features in a single DataFrame row
        feature_df = pd.DataFrame([{
            "fixed_acidity": fixed_acidity,
            "volatile_acidity": volatile_acidity,
            "citric_acid": citric_acid,
            "residual_sugar": residual_sugar,
            "chlorides": chlorides,
            "free_sulfur_dioxide": free_sulfur_dioxide,
            "total_sulfur_dioxide": total_sulfur_dioxide,
            "density": density,
            "pH": pH,
            "sulphates": sulphates,
            "alcohol": alcohol,
            "color": color  # might need encoding if your model expects numeric
        }])
        
        # Predict
        prediction = model.predict(feature_df)[0]
        
        # Return the same page but show the prediction
        return render_template("model_pred_manual.html", prediction=prediction)

    # If GET, just show the form
    return render_template("model_pred_manual.html")

if __name__ == "__main__":
    app.run(debug=True)
