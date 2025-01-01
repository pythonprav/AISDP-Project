#!/bin/bash

# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build the Docker image
docker build -t model-training:latest -f Model-Training/Model\ Training\ Dockerfile.dockerfile .

# Deploy PV and PVC
kubectl apply -f pv-pvc.yaml

# Deploy the model training service
kubectl apply -f model-training-deployment.yaml

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=model-training --timeout=120s

# Expose the service and display the URL
minikube service model-training-service --url
