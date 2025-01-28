# AISDP Project: Wine Quality Prediction
This project is an end-to-end machine learning pipeline to predict wine quality based on its physicochemical properties. It includes multiple modules for data preprocessing, model training, inference, and a web application for user interaction. The goal is to demonstrate the integration of AI with modular, scalable, and efficient coding practices.

## Directory Structure
```bash
.
├── README.md                     # Project documentation
├── data                          # Data directory
│   ├── cleaned_wine_quality.csv  # Preprocessed dataset
│   ├── wine_quality.json         # JSON representation of the original dataset
│   └── wine_quality_assignment.csv  # Original wine quality dataset
├── data-preprocessing            # Data preprocessing module
│   ├── Dockerfile                # Dockerfile to containerize preprocessing
│   ├── convert_csv_to_json.py    # Script to convert CSV to JSON
│   ├── preprocess.py             # Flask API for data preprocessing
│   └── test_preprocess.py        # Unit tests for preprocessing
├── model-inference               # Model inference module
│   ├── Dockerfile                # Dockerfile to containerize inference
│   ├── inference.py              # Flask API for making predictions
│   └── test_inference.py         # Unit tests for inference
├── model-training                # Model training module
│   ├── Dockerfile                # Dockerfile to containerize model training
│   ├── optimized_rf_model.pkl    # Saved optimized Random Forest model
│   └── train_model.py            # Script to train the Random Forest model
├── requirements.txt              # Python dependencies
└── web-application               # Web application for user interaction
    ├── Dockerfile                # Dockerfile to containerize the web app
    └── winequality_app.py        # Flask app for wine quality predictions
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