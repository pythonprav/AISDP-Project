#!/bin/bash

# Clean up any previous resources
echo "Cleaning up previous resources..."
kubectl delete deployment --all
kubectl delete service --all
kubectl delete pvc --all
kubectl delete pv --all

# 1. Data Preprocessing Container
echo "Building and deploying the data-preprocessing container..."

# Build and push the data-preprocessing Docker image
cd data-preprocessing
docker build -t pariikubavat/data-preprocessing:latest -f data_preprocessing.dockerfile .
docker push pariikubavat/data-preprocessing:latest
cd ..

# Apply PVC, deployment, and service for data-preprocessing
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment-data-preprocessing.yaml
kubectl apply -f k8s/service-data-preprocessing.yaml

# Wait for the data-preprocessing container to be ready (optional: adjust time)
kubectl wait --for=condition=ready pod --selector=app=data-preprocessing --timeout=300s

# Trigger the data-preprocessing process (use port-forwarding for local testing)
kubectl port-forward service/data-preprocessing-service 5004:5004 & 
sleep 5 
curl -X GET http://localhost:5004/get-data

# Wait for data-preprocessing to complete (check logs if needed)
echo "Waiting for data-preprocessing to complete..."
sleep 10  # Wait for the preprocessing to finish

# Check the output
kubectl exec -it $(kubectl get pods --selector=app=data-preprocessing -o=jsonpath='{.items[0].metadata.name}') -- ls /app/volumes/data

# 2. Model Training Container
echo "Building and deploying the model-training container..."

# Build and push the model-training Docker image
cd model-training
docker build -t pariikubavat/model-training:latest -f model_training.dockerfile .
docker push pariikubavat/model-training:latest
cd ..

# Apply the deployment and service for model-training
kubectl apply -f k8s/deployment-model-training.yaml
kubectl apply -f k8s/service-model-training.yaml
sleep 60

# Wait for the model-training container to be ready
kubectl wait --for=condition=ready pod --selector=app=model-training --timeout=300s
sleep 60

# Trigger the model training process (this might require a curl or internal command depending on the setup)
# Here we check the logs to make sure it’s running correctly
kubectl logs $(kubectl get pods --selector=app=model-training -o=jsonpath='{.items[0].metadata.name}')
sleep 60

# Check if model has been saved (saved_model.pkl)
kubectl exec -it $(kubectl get pods --selector=app=model-training -o=jsonpath='{.items[0].metadata.name}') -- ls /app/volumes/models/

# 3. Model Inference Container
echo "Building and deploying the model-inference container..."

# Build and push the model-inference Docker image
cd model-inference
docker build -t pariikubavat/model-inference:latest -f model_inference.dockerfile .
docker push pariikubavat/model-inference:latest
cd ..

# Apply the deployment and service for model-inference
kubectl apply -f k8s/deployment-model-inference.yaml
kubectl apply -f k8s/service-model-inference.yaml

# Wait for the model-inference container to be ready
kubectl wait --for=condition=ready pod --selector=app=model-inference --timeout=300s

# Trigger the model inference process (this might involve input file check or trigger from service)
# Here we check if the model inference is accessible via curl
kubectl port-forward service/model-inference 5001:5001 & 
sleep 5
curl -X POST http://localhost:5001/predict

# Check the output for the predictions

# 4. User Interface Container
echo "Building and deploying the user-interface container..."

# Build and push the user-interface Docker image
cd user-interface
docker build -t pariikubavat/user-interface:latest -f web_application.dockerfile .
docker push pariikubavat/user-interface:latest
cd ..

# Apply the deployment and service for user-interface
kubectl apply -f k8s/deployment-user-interface.yaml
kubectl apply -f k8s/service-user-interface.yaml

# Wait for the user-interface container to be ready
kubectl wait --for=condition=ready pod --selector=app=user-interface --timeout=300s

# Trigger the user interface functionality
# Check the user interface status (curl or access UI as needed)
kubectl port-forward service/user-interface-service 5003:5003 &

