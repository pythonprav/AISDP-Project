#!/bin/bash

# Decode the base64-encoded token
GITHUB_TOKEN=$(echo "Z2l0aHViX3BhdF8xMUJBWEhDNVEwUjl5em9NZ3RRbGJ2X2dxcWR5YVIwdWRXZTY1N3pKcWhCTjRNc3lqTEFDR0d6SXkwMVpwN0FsUHoySURaRERYTEJlbTI5TjBF" | base64 --decode)
git clone --branch pravallika-branch https://pythonprav:${GITHUB_TOKEN}@github.com/pythonprav/AISDP-Project.git

export GITHUB_TOKEN= Z2l0aHViX3BhdF8xMUJBWEhDNVEwUjl5em9NZ3RRbGJ2X2dxcWR5YVIwdWRXZTY1N3pKcWhCTjRNc3lqTEFDR0d6SXkwMVpwN0FsUHoySURaRERYTEJlbTI5TjBF

# Export environment variables
export ROLLBACK_ENABLED=true
export TRAINING_FILE_PATH="./Data/wine_quality_assignment.csv"
export LOG_LEVEL=DEBUG

# Start the Flask server for model training
python ./Model-Training/train_model.py


# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build the Docker image
docker build -t model-training:latest -f Model-Training/Model\ Training\ Dockerfile.dockerfile .
docker tag model-training:latest pravallikadocker123/model-training:latest
docker push pravallikadocker123/model-training:latest


# Deploy PV and PVC
kubectl apply -f pv-pvc.yaml

# Deploy the model training service
kubectl apply -f model-training-deployment.yaml

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=model-training --timeout=120s

# Expose the service and display the URL
minikube service model-training-service --url
