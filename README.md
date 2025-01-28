# AISDP Project: Wine Quality Prediction
This project is an end-to-end machine learning pipeline to predict wine quality based on its physicochemical properties. It includes multiple modules for data preprocessing, model training, inference, and a web application for user interaction. The goal is to demonstrate the integration of AI with modular, scalable, and efficient coding practices.

## Directory Structure
```bash
.
├── README.md                              # Project documentation
├── data                                   # Dataset and feature-related files
│   ├── cleaned_wine_quality.csv          # Cleaned and preprocessed dataset
│   ├── feature_names.csv                 # Extracted feature names for inference
│   ├── wine_quality.json                 # JSON format of the original dataset
│   └── wine_quality_assignment.csv       # Original raw dataset
├── data-preprocessing                    # Data preprocessing module
│   ├── Dockerfile                        # Docker configuration for preprocessing
│   ├── convert_csv_to_json.py            # Script to convert CSV to JSON format
│   ├── preprocess.py                     # Flask app for preprocessing
│   └── test_preprocess.py                # Unit tests for the preprocessing module
├── model-inference                       # Model inference module
│   ├── Dockerfile                        # Docker configuration for inference
│   ├── generate_feature_names.py         # Script to extract feature names
│   ├── inference.py                      # Flask app for inference
│   └── test_inference.py                 # Unit tests for the inference module
├── model-training                        # Model training module
│   ├── Dockerfile                        # Docker configuration for training
│   ├── optimized_rf_model.pkl            # Trained Random Forest model
│   └── train_model.py                    # Script for training the Random Forest model
├── requirements.txt                      # Python dependencies for the project
└── web-application                       # Web application module
    ├── Dockerfile                        # Docker configuration for the web app
    └── winequality_app.py                # Flask app for serving the web application
```

## Setup Instructions
1. **Python Version:** Ensure Python 3.12.x is installed.
2. **Dependencies:** Install required packages using:

```bash
pip install -r requirements.txt
```

3. **Docker:** Install Docker to containerize and run the modules.

## 1. Data Preprocessing
The data-preprocessing module cleans and prepares the raw dataset.

### Files
**Dockerfile:** Sets up the container environment.

**convert_csv_to_json.py:** Converts wine_quality_assignment.csv into JSON format.

**preprocess.py:** 
- A Flask app that accepts JSON data and performs preprocessing.
- Saves cleaned data to data/cleaned_wine_quality.csv.

**test_preprocess.py:** Contains unit tests for preprocessing.

### Steps
1. **Convert CSV to JSON:**
   
```bash
python data-preprocessing/convert_csv_to_json.py
```

2. **Run Flask App:**
   
```bash
python data-preprocessing/preprocess.py
```

3. **Using curl:**
   
```bash
curl -X POST -H "Content-Type: application/json" \
-d @data/wine_quality.json \
http://127.0.0.1:5000/get-data
```

- The cleaned dataset is saved automatically to data/cleaned_wine_quality.csv.
- Flask is used to allow flexible preprocessing via API calls.
- Docker can be used to containerize the preprocessing workflow (optional).

## 2. Model Training
The model training component is responsible for building, optimizing, and saving a Random Forest model to predict wine quality based on preprocessed data.

### Files
**train_model.py:** The main script for training the Random Forest model.

**optimized_rf_model.pkl:** The saved, optimized Random Forest model.

**Dockerfile:** Instructions to containerize the model training environment.

The optimized Random Forest model is saved as optimized_rf_model.pkl in the model-training/ directory for use in inference.

## 3. Model Inference
The model-inference module is responsible for using the trained model to make predictions based on new data.

### Files
**Dockerfile:** Sets up the container environment for the inference module.

**generate_feature_names.py:** 
- Extracts the feature names from the preprocessed dataset.
- Saves the feature names to data/feature_names.csv.

  **inference.py::** 
- Loads the trained model (model-training/optimized_rf_model.pkl).
- Uses feature names to validate input data and ensure correct format.
- Returns predictions for input JSON data.

**test_inference.py:** Contains a test script that sends a JSON payload to the inference API and validates the response.

### Steps
1. **Extract Feature Names:**
   
```bash
python model-inference/generate_feature_names.py
```

2. **Run the Flask Inference API:**
   
```bash
python model-inference/inference.py
```

3. **Send a Prediction Request:**
   
```bash
curl -X POST -H "Content-Type: application/json" \
-d @data/wine_quality.json \
http://127.0.0.1:5000/predict
```

**Example Response:**

```bash
{
    "message": "Prediction successful",
    "predictions": [3, 4, 3, 3, 2]
}
```
### Output
- Feature Names: data/feature_names.csv.
- Predictions: Returned as a JSON response from the inference API.
- The inference module uses the trained Random Forest model to make accurate predictions.