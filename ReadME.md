
AISDP-Project

├── .pytest_cache
├── data-preprocessing
│   ├── raw_data
│   │   └── wine_quality_assignment.csv
│   ├── data_preprocessing.dockerfile
│   ├── preprocess.py
│   └── requirements.txt
├── k8s
│   ├── data-preprocessing-deployment.yaml
│   ├── data-preprocessing-service.yaml
│   ├── model-inference-deployment.yaml
│   ├── model-inference-service.yaml
│   ├── model-training-deployment.yaml
│   ├── pvc.yaml
│   ├── raw-data-pvc.yaml
│   ├── user-interface-deployment.yaml
│   └── user-interface-service.yaml
├── model-inference
│   ├── inference.py
│   ├── model_inference.dockerfile
│   └── requirements.txt
├── model-training
│   ├── model_training.dockerfile
│   ├── requirements.txt
│   └── train_model.py
├── user-interface
│   ├── static
│   │   ├── css
│   │   └── js
│   ├── templates
│   │   ├── index.html
│   │   ├── model_pred_csv.html
│   │   └── model_pred_manual.html
│   ├── requirements.txt
│   ├── web_application.dockerfile
│   └── winequality_app.py
├── volumes
│   ├── data
│   │   ├── cleaned_wine_quality.csv
│   │   └── wine_quality.json
│   ├── models
│   │   └── saved_model.pkl
│   └── user
│       ├── cleaned_input.csv
│       ├── input.csv
│       └── predictions.json
└── README.md
└── run.sh

# **README: Wine Quality Prediction - Model Training Container**  

---

## **1. Overview**  
The Wine Quality Prediction project is designed to predict wine quality using a machine learning model trained with a **RandomForestClassifier**. The project is containerized using **Docker** for consistency and deployed using **Kubernetes** for scalability and reliability. The dataset is preprocessed and saved as `cleaned_wine_quality.csv` in the `/data` folder, and the trained model is saved as `saved_model.pkl` in the `/models` folder. Hyperparameter tuning is performed using **GridSearchCV** to optimize model performance. Persistent storage volumes ensure that input data and trained models are accessible even after the container stops.

---

## **2. File Structure**  

```plaintext
model-training
├── data                           # Input data folder
│   └── cleaned_wine_quality.csv   # Cleaned dataset used for training
├── models                         # Output model folder
│   └── saved_model.pkl            # Trained RandomForest model (Pickle file)
├── k8s                            # Kubernetes configuration files
│   └── model-training-deployment.yaml  # Kubernetes deployment for model training
├── model_training.dockerfile      # Dockerfile to build the training container
├── requirements.txt               # Dependencies for the training container
└── train_model.py                 # Core script for training the model
```

- **`data/cleaned_wine_quality.csv`**: The cleaned dataset used as input for model training.  
- **`models/saved_model.pkl`**: The trained RandomForest model saved as a pickle file.  
- **`k8s/model-training-deployment.yaml`**: Kubernetes deployment file that automates the execution of the model training container.  
- **`model_training.dockerfile`**: Dockerfile that defines the container environment and ensures all dependencies are installed.  
- **`requirements.txt`**: Lists the dependencies required for model training, including **pandas**, **numpy**, **scikit-learn**, and **joblib**.  
- **`train_model.py`**: The core script responsible for loading the dataset, training the model, evaluating performance, and saving the trained model.

---

## **3. Project Architecture**  

1. **Data Loading:** The dataset `cleaned_wine_quality.csv` is loaded from `/data` using **pandas.read_csv()**.  
2. **Data Splitting:** The dataset is split into training and testing sets using **train_test_split()** with an 80-20 split.  
3. **Model Training:** A **RandomForestClassifier** is trained using **GridSearchCV** to optimize hyperparameters such as `n_estimators`, `max_depth`, `min_samples_split`, `min_samples_leaf`, and `max_features`.  
4. **Performance Evaluation:** The model is evaluated using **accuracy_score** and **classification_report**.  
5. **Model Saving:** The trained model is saved as `saved_model.pkl` in `/models` using **pickle.dump()**.  

---

## **4. Data Flow**  

```plaintext
           Input: data/cleaned_wine_quality.csv
                      |
                      v
         +--------------------------------+
         | train_model.py                 |
         | - Loads dataset using pandas   |
         | - Splits data into train/test  |
         | - Trains RandomForest model    |
         | - Saves model using pickle     |
         +--------------------------------+
                      |
                      v
           Output: models/saved_model.pkl
```

- The dataset is loaded from **`/data/cleaned_wine_quality.csv`**.  
- The trained model is saved in **`/models/saved_model.pkl`**.  

---

## **5. Features & Functionalities**  

✅ **RandomForestClassifier:** Predicts wine quality using optimized hyperparameters.  
✅ **GridSearchCV:** Performs hyperparameter tuning with cross-validation to find the best model configuration.  
✅ **Docker Container:** Ensures a consistent environment for training the model.  
✅ **Persistent Storage:** Stores input data and trained models in shared volumes for accessibility.  
✅ **Kubernetes Deployment:** Automates the execution and scaling of the training container.  

---

## **6. Dependencies**  

The following dependencies are listed in **`requirements.txt`**:  

- **flask==3.0.0**: For potential API deployment.  
- **pandas==2.1.0**: For loading and manipulating data.  
- **numpy==1.26.0**: For numerical operations.  
- **scikit-learn**: For machine learning and evaluation.  
- **joblib**: For parallel processing during model training.  

---

## **7. Docker Implementation**  

- **Dockerfile (model_training.dockerfile):**  
  - The Dockerfile installs the dependencies listed in **`requirements.txt`**.  
  - It copies the **`train_model.py`** script into the container and sets it as the entry point.  
  - The working directory is set to `/app`, where the script is executed.  

- **Volume Mounts:**  
  - The **`/data`** folder is mounted to provide access to the input dataset.  
  - The **`/models`** folder is mounted to save the trained model.  

### **Docker Workflow:**  
1. **Build the Docker Image:**  
   - The image is built using the command:  
   ```bash
   docker build -t model-training -f model_training.dockerfile .
   ```

2. **Run the Docker Container:**  
   - The container is executed using the command:  
   ```bash
   docker run --rm -v $(pwd)/data:/data -v $(pwd)/models:/models model-training
   ```

---

## **8. Kubernetes Deployment**  

- **Deployment File (model-training-deployment.yaml):**  
  - The deployment is configured as a Kubernetes **Job** that runs the container once and then terminates.  
  - Persistent volumes are mounted to ensure access to input data and output models.  
  - Environment variables **`DATA_PATH`** and **`MODEL_PATH`** are used to specify file paths within the container.  

### **Volume Mounts:**  
- The `/data` volume provides access to **`cleaned_wine_quality.csv`**.  
- The `/models` volume is used to save **`saved_model.pkl`**.  

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

The **`train_model.py`** script is responsible for the entire model training process. It performs the following steps:

1. **Load Data:**  
   - The script reads the dataset from `/data/cleaned_wine_quality.csv` using **pandas.read_csv()**.

2. **Data Splitting:**  
   - The dataset is split into training and testing sets using **train_test_split()** with an 80-20 split and `random_state=42` for reproducibility.

3. **Model Training:**  
   - A **RandomForestClassifier** is trained using **GridSearchCV** to optimize the following hyperparameters:  
     - `n_estimators`: 100, 150  
     - `max_depth`: 20, None  
     - `min_samples_split`: 2, 4  
     - `min_samples_leaf`: 1, 2  
     - `max_features`: 'sqrt', 'log2'  

4. **Performance Evaluation:**  
   - The model is evaluated using **accuracy_score** and **classification_report**.  
   - The classification report includes precision, recall, and F1-score for each class.

5. **Save Model:**  
   - The trained model is saved as **`saved_model.pkl`** in the `/models` folder using **pickle.dump()**.

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
- **Class 3** has the highest performance, with an F1-Score of **0.92** and Recall of **0.98**, indicating that the model is highly accurate in predicting this class.  
- **Class 1** and **Class 2** have lower Recall, which may be due to the smaller number of samples (Support = 3 and 44, respectively).  
- The **Weighted Average F1-Score** of **0.84** demonstrates that the model performs well overall, considering class imbalance.

---

## **12. Conclusion**  

The Wine Quality Prediction project successfully automates the training process using a **RandomForestClassifier** with hyperparameter tuning. The combination of **Docker** and **Kubernetes** ensures that the training process is consistent, scalable, and reliable. Input data is loaded from **`/data/cleaned_wine_quality.csv`**, and the trained model is saved as **`/models/saved_model.pkl`**. Using **Persistent Volumes**, both the input data and trained model remain accessible even after the container stops, making this pipeline suitable for production use.





