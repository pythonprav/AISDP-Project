# **EGT309 AI Solution Development Project**

## Project: Determine Wine Quality
This project is a Kubernetes-based machine learning system to determine wine quality in a fully containerized enviornment with persistent storage, as well as a user-friendly web interface

## System Architecture
- Data Preprocessing: Cleans & Transform raw data
- Model Training: Trains a predictive model using Machine Learning
- Model Inference: use the trained model to make predictions
- User Interface: web application for user to interact

## Deployment Containers & Services

### Data Preprocessing
- Description: Clean and transform raw CSV data
- Deployment YAML: <code>data-preprocessing-deployment.yaml<code>
- Service YAML: <code>data-preprocessing-servicce.yaml<code>

### Model Training
- Description:
- Deployment YAML: 
- Service YAML: N/A

### Model Inference
- Description:
- Deployment YAML: 
- Service YAML: N/A

### User Interface:
- Description:
- Deployment YAML: 
- Service YAML: N/A

## File Structure
📦AISDP-Project

┣ 📂.github

 ┃ ┗ 📂workflows

 ┣ 📂backup data

 ┣ 📂data-preprocessing

 ┃ ┣ 📂data

 ┃ ┣ 📂raw_data

 ┃ ┃ ┗ 📜wine_quality_assignment.csv

 ┃ ┣ 📂__pycache__

 ┃ ┣ 📜data_preprocessing.dockerfile

 ┃ ┣ 📜preprocess.py

 ┃ ┗ 📜requirements.txt

 ┣ 📂k8s

 ┃ ┣ 📜data-preprocessing-deployment.yaml

 ┃ ┣ 📜data-preprocessing-service.yaml

 ┃ ┣ 📜model-inference-deployment.yaml

 ┃ ┣ 📜model-inference-service.yaml

 ┃ ┣ 📜model-training-deployment.yaml

 ┃ ┣ 📜pvc.yaml

 ┃ ┣ 📜raw-data-pvc.yaml

 ┃ ┣ 📜user-interface-deployment.yaml

 ┃ ┗ 📜user-interface-service.yaml

 ┣ 📂kubernetes

 ┣ 📂mnt

 ┃ ┣ 📂models

 ┃ ┣ 📂raw_data

 ┃ ┗ 📂user

 ┣ 📂model-inference

 ┃ ┣ 📜inference.py

 ┃ ┣ 📜model_inference.dockerfile

 ┃ ┗ 📜requirements.txt

 ┣ 📂Model-Training

 ┃ ┣ 📂redundant

 ┃ ┣ 📜model_training.dockerfile

 ┃ ┣ 📜requirements.txt

 ┃ ┗ 📜train_model.py

 ┣ 📂raw_data

 ┣ 📂user-interface

 ┃ ┣ 📂assets

 ┃ ┃ ┣ 📂css

 ┃ ┃ ┗ 📂js

 ┃ ┣ 📂static

 ┃ ┃ ┣ 📂css

 ┃ ┃ ┃ ┗ 📜style.css

 ┃ ┃ ┗ 📂js

 ┃ ┃ ┃ ┗ 📜script.js

 ┃ ┣ 📂templates

 ┃ ┃ ┣ 📜index.html

 ┃ ┃ ┣ 📜model_pred_csv.html

 ┃ ┃ ┗ 📜model_pred_manual.html

 ┃ ┣ 📜requirements.txt

 ┃ ┣ 📜web_application.dockerfile

 ┃ ┗ 📜winequality_app.py

 ┣ 📂volumes

 ┃ ┣ 📂data

 ┃ ┃ ┣ 📜.DS_Store

 ┃ ┃ ┣ 📜cleaned_wine_quality.csv

 ┃ ┃ ┗ 📜wine_quality.json

 ┃ ┣ 📂models

 ┃ ┃ ┗ 📜saved_model.pkl

 ┃ ┣ 📂user

 ┃ ┃ ┣ 📜cleaned_input.csv

 ┃ ┃ ┣ 📜input.csv

 ┃ ┃ ┗ 📜predictions.json

 ┃ ┣ 📂userinput

 ┃ ┗ 📜.DS_Store

 ┣ 📜.DS_Store

 ┣ 📜REAME.md

 ┗ 📜run.sh
 

