# **EGT309 AI Solution Development Project: Team Harvard**
GitHub Repository: https://github.com/pythonprav/AISDP-Project

## Project: Determine Wine Quality
This project is a Kubernetes-based machine learning system to determine wine quality in a fully containerized enviornment with persistent storage, as well as a user-friendly web interface

## System Architecture
- Data Preprocessing: Cleans & Transform raw data
- Model Training: Trains a predictive model using Machine Learning
- Model Inference: Uses the trained model + UI cleaned input csv to make wine quality predictions
- User Interface: Web application for user to interact

## System Workflow
**PHASE 1: MODEL PREPARATION**

**Data Preprocessing:**
- Input: wine_quality_assignment.csv
- Output: cleaned_wine_quality.csv, wine_quality.json

**Model Training:** 
-	Input: cleaned_wine_quality.csv
-	Output: saved_model.pkl

**PHASE 2: MODEL DEPLOYMENT & INFERENCE**

**User Interface**
-	User uploads: input.csv
  
**Data Preprocessing (User Input)**
	•	Input: input.csv
	•	Output: cleaned_input.csv

**Model Inference**
-	Input: cleaned_input.csv, saved_model.pkl
-	Output: predictions.json

**User Interface (Results Display)**
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

## Model Training Container (model-training)

## **3. Project Architecture**  

1. **Data Loading:** The dataset `cleaned_wine_quality.csv` is loaded from `/data` using **pandas.read_csv()**.  
2. **Data Splitting:** The dataset is split into training and testing sets using **train_test_split()** with an 80-20 split.  
3. **Model Training:** A **RandomForestClassifier** is trained using **GridSearchCV** to optimize hyperparameters.  
4. **Performance Evaluation:** The model is evaluated using **accuracy_score** and **classification_report**.  
5. **Model Saving:** The trained model is saved as `saved_model.pkl` in `/models` using **pickle.dump()**.  

---

## **4. Data Flow**  
![Image](https://github.com/user-attachments/assets/0e281b20-8855-4d4e-913d-7217fead78d6)

- The dataset is loaded from `/data/cleaned_wine_quality.csv`.  
- The trained model is saved in `/models/saved_model.pkl`.  

---

## **5. Features & Functionalities**  

- **RandomForestClassifier:** Predicts wine quality using optimized hyperparameters.  
- **GridSearchCV:** Performs hyperparameter tuning with cross-validation to find the best model configuration.  
- **Docker Container:** Ensures a consistent environment for training the model.  
- **Persistent Storage:** Stores input data and trained models in shared volumes for accessibility.  
- **Kubernetes Deployment:** Automates the execution and scaling of the training container.  

---

## **6. Dependencies**  

The following dependencies are listed in `requirements.txt`:  

- **flask==3.0.0:** For potential API deployment.  
- **pandas==2.1.0:** For loading and manipulating data.  
- **numpy==1.26.0:** For numerical operations.  
- **scikit-learn:** For machine learning and evaluation.  
- **joblib:** For parallel processing during model training.  

---

## **7. Docker Implementation**  

- **Dockerfile (model_training.dockerfile):**  
  - Installs the dependencies listed in `requirements.txt`.  
  - Copies the `train_model.py` script into the container and sets it as the entry point.  
  - Sets the working directory to `/app`, where the script is executed.  

- **Volume Mounts:**  
  - The `/data` folder is mounted to provide access to the input dataset.  
  - The `/models` folder is mounted to save the trained model.  

### **Docker Workflow:**  
1. **Build the Docker Image:**  
   ```bash
   docker build -t model-training -f model_training.dockerfile .
   ```
2. **Run the Docker Container:**  
   ```bash
   docker run --rm -v $(pwd)/data:/data -v $(pwd)/models:/models model-training
   ```

---

## **8. Kubernetes Deployment**  

- **Deployment File (model-training-deployment.yaml):**  
  - Configured as a Kubernetes **Job** that runs the container once and then terminates.  
  - Persistent volumes are mounted to ensure access to input data and output models.  
  - Environment variables `DATA_PATH` and `MODEL_PATH` specify file paths within the container.  

### **Volume Mounts:**  
- `/data` provides access to `cleaned_wine_quality.csv`.  
- `/models` is used to save `saved_model.pkl`.  

### **Kubernetes Workflow:**  
1. **Apply the Deployment File:**  
   ```bash
   kubectl apply -f k8s/model-training-deployment.yaml
   ```
2. **Monitor the Job Logs:**  
   ```bash
   kubectl logs job/model-training
   ```

---

## **9. Model Training Process (train_model.py)**  

![Image](https://github.com/user-attachments/assets/6e2479e5-4503-4b2d-b39d-bb835dec6ae5)


The `train_model.py` script handles the model training process:

1. **Load Data:**  
   - Reads the dataset from `/data/cleaned_wine_quality.csv` using **pandas.read_csv()**.
2. **Data Splitting:**  
   - Splits the dataset into training and testing sets using **train_test_split()** with an 80-20 split and `random_state=42` for reproducibility.
3. **Model Training:**  
   - Trains a **RandomForestClassifier** using **GridSearchCV** to optimize hyperparameters.
4. **Performance Evaluation:**  
   - Evaluates the model using **accuracy_score** and **classification_report**.
5. **Save Model:**  
   - Saves the trained model as `saved_model.pkl` in the `/models` folder using **pickle.dump()**.

---

## **10. Communication Between Container & Data Storage**  

1. **Persistent Volumes:**  
   - The `/data` volume stores the input dataset, making it accessible to the training script.  
   - The `/models` volume stores the trained model, ensuring it is available even after the container stops.
2. **Volume Mounts:**  
   - The host system's `/data` and `/models` folders are mounted inside the container for seamless data access.
3. **Environment Variables:**  
   - `DATA_PATH` specifies the location of the input dataset: `/data/cleaned_wine_quality.csv`.  
   - `MODEL_PATH` specifies the location to save the trained model: `/models/saved_model.pkl`.

---

## **11. Model Performance Summary**  

### **Training Results**
- **Accuracy:** 0.87 (87%)  
- **Best Hyperparameters:**  
  - `max_depth=None`  
  - `max_features='log2'`  
  - `min_samples_leaf=2`  

### **Classification Report:**  
| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| **1** | 1.00     | 0.00   | 0.00     | 3       |
| **2** | 0.75     | 0.07   | 0.12     | 44      |
| **3** | 0.87     | 0.98   | 0.92     | 1003    |
| **4** | 0.81     | 0.57   | 0.67     | 212     |
| **5** | 0.91     | 0.57   | 0.70     | 37      |

- **Macro Average:** Precision: 0.87, Recall: 0.44, F1-Score: 0.48  
- **Weighted Average:** Precision: 0.86, Recall: 0.87, F1-Score: 0.84  

### **Insights:**  
- **Class 3** has the highest performance, with an F1-Score of **0.92** and Recall of **0.98**.
- **Class 1** and **Class 2** have lower Recall, likely due to the smaller number of samples (Support = 3 and 44, respectively).  
- The **Weighted Average F1-Score** of **0.84** demonstrates strong overall model performance considering class imbalance.

---

### Future Improvements:
If there were more time and scope, I would implement my retrain feature from my old code and allow users to edit training parameters directly from the UI, with a button to train and a window to display training metrics.


## Model Inference Container (model-inference)
### File Structure
```plaintext
├── model-inference
│   ├── inference.py
│   ├── model_inference.dockerfile
│   └── requirements.txt
├── k8s
│   ├── user-interface-deployment.yaml
│   └── user-interface-service.yaml
```
