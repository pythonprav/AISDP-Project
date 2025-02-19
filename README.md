# **EGT309 AI Solution Development Project: Team Harvard**


## Project: Determine Wine Quality
This project is a Kubernetes-based machine learning system to determine wine quality in a fully containerized enviornment with persistent storage, as well as a user-friendly web interface

## System Architecture
- Data Preprocessing: Cleans & Transform raw data
- Model Training: Trains a predictive model using Machine Learning
- Model Inference: Uses the trained model + UI cleaned input csv to make wine quality predictions
- User Interface: Web application for user to interact

## System Workflow
**PHASE 1: MODEL PREPARATION**

Data Preprocessing:
- Input: wine_quality_assignment.csv
- Output: cleaned_wine_quality.csv, wine_quality.json

Model Training: 
-	Input: cleaned_wine_quality.csv
-	Output: saved_model.pkl

**PHASE 2: MODEL DEPLOYMENT & INFERENCE**
User Interface
-	User uploads: input.csv
  
Data Preprocessing (User Input)
	•	Input: input.csv
	•	Output: cleaned_input.csv

Model Inference
-	Input: cleaned_input.csv, saved_model.pkl
-	Output: predictions.json

User Interface (Results Display)
- Display predictions.json
 
## Deployment Containers & Services

### Data Preprocessing
- Description: Clean and transform raw CSV data
- Deployment YAML: deployment-data-preprocessing.yaml
- Service YAML: service-data-preprocessing.yaml

### Model Training
- Description: Train ML model using cleaned data
- Deployment YAML: deployment-model-training.yaml
- Service YAML: service-model-training.yaml

### Model Inference
- Description: Used trained model to predict wine quality
- Deployment YAML: deployment-model-inference.yaml
- Service YAML: service-model-inference.yaml

### User Interface:
- Description: Provides an interactive web app
- Deployment YAML: deployment-user-interface.yaml
- Service YAML: service-user-interface.yaml

## File Structure
```plaintext
.
├── data-preprocessing
│   ├── data_preprocessing.dockerfile
│   ├── preprocess.py
│   ├── raw_data
│   │   └── wine_quality_assignment.csv
│   └── requirements.txt
├── k8s
│   ├── deployment-data-preprocessing.yaml
│   ├── deployment-model-inference.yaml
│   ├── deployment-model-training.yaml
│   ├── deployment-user-interface.yaml
│   ├── pvc.yaml
│   ├── service-data-preprocessing.yaml
│   ├── service-model-inference.yaml
│   ├── service-model-training.yaml
│   └── service-user-interface.yaml
├── model-inference
│   ├── inference.py
│   ├── model_inference.dockerfile
│   ├── requirements.txt
│   └── volumes
│       ├── models
│       └── user
├── model-training
│   ├── model_training.dockerfile
│   ├── requirements.txt
│   └── train_model.py
├── run.sh
├── setup_storage.sh
├── user-interface
│   ├── requirements.txt
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       └── script.js
│   ├── templates
│   │   ├── index.html
│   │   ├── model_pred_csv.html
│   │   └── model_pred_manual.html
│   ├── web_application.dockerfile
│   └── winequality_app.py
└── volumes
    ├── data
    │   ├── cleaned_wine_quality.csv
    │   └── wine_quality.json
    ├── models
    │   └── saved_model.pkl
    └── user
        ├── cleaned_input.csv
        ├── input.csv
        └── predictions.json
```

## Data Preprocessing Container (data-preprocessing)
### Overview

The Data Preprocessing COntainer is designed to clean the raw CSV file from the training data and user input data (uploading a CSV or manual input through the UI)

Steps:
- Drop Unnecessary Columns
- Drop NaN values
- Drop Duplicates
- Format Numeric columns
- Encode categorical features
- Map target labels to a specific scale
- Prepare cleaned dataset for other tasks in the pipeline

This container is important in ensuring quality and consistent data in this pipeline.

### File Structure
```plaintext
├── data-preprocessing
│   ├── data_preprocessing.dockerfile
│   ├── preprocess.py
│   ├── raw_data
│   │   └── wine_quality_assignment.csv
│   └── requirements.txt
```

### Project Architecture
This section is deployed in a Kubernetes environment with the following configuration
- Deployment Configuration (defined in data-preprocessing.yaml)
    - /app/volumes/data: store cleaned dataset
    - /app/volumes/user: holds user related data

- Service Configuration (defined in data-preprocessing-service.yaml)
    - exposes the Data Preprocessing service at http://data-preprocessing-service:5004, which allows other containers to access it

- Volume Mounts
    - /app/volumes/data pushed to data-volume-pvc to store cleaned dataset
    - /app/volumes/user pushed to user-volume-pvc to store user uploaded data

### Data Flow Diagram
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image.png)

### Features & Functionalities
**Main Preprocessing Steps**
- Training data "wine_quality_assignment.csv" was retrieved from the "raw_data" folder
- Dropped "Sample" column
- Dropped NaN values, duplicates, outliers
- Format numeric columns to ensure correct data types
- Encode categorical features (White - 0, Red - 1)
- Maps "quality" from 1 to 5

**User Input Methods**
- CSV input: user can upload a CSV file through the UI, which is sent fromt he <code>/upload_csv</code> route
- Manual input: user can manually enter the wine features through the UI

**Output from Data Preprocessing**

Cleaned datasets saved in /app/volumes/data or /app/volumes/user as:
- cleaned_wine_quality.csv
- cleaned_input.csv

### preprocess.py
This script handles data preprocessing using Flask API
- /get-data: preprocess the training dataset and saves the cleaned version
- /process-user-input: preprocess the data uploaded by the user and save it as cleaned_input.csv

**convert_csv_to_json()**: convert raw CSV to JSON

**clean_column(column)**: define cleaning numeric columns by removing non-numeric characters

**preprocess_data_logic(df)**: main preprocessing function

### data_preprocessing.dockerfile
- Base Image: <code>python:3.9-slim</code>
- Steps:
    - install dependencies from <code>requirements.txt</code>
    - set up necessary directories for volume mount
    - expose port 5004 for API
    - start Flask application using "python preprocess.py" command

