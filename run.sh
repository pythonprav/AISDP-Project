#!/bin/bash

echo "Starting User Interface Deployment"

# Step 1: Delete old UI resources
echo "Deleting old UI resources..."
kubectl delete deployment user-interface --ignore-not-found
kubectl delete service user-interface-service --ignore-not-found

# Step 2: Build and Push UI Docker Image
echo "Building and Pushing UI Docker Image..."
cd user-interface
docker build -t pariikubavat/user-interface:latest -f web_application.dockerfile .
docker push pariikubavat/user-interface:latest
cd ..

# Step 3: Deploy UI in Kubernetes
echo "Applying UI Deployment and Service..."
kubectl apply -f k8s/user-interface-deployment.yaml
kubectl apply -f k8s/user-interface-service.yaml

# Step 4: Wait for UI Pod to be Ready
echo "Waiting for UI pod to be ready..."
kubectl wait --for=condition=ready pod -l app=user-interface --timeout=120s

# Step 5: Port Forward UI to Localhost
echo "Port Forwarding UI to localhost:5003"
kubectl port-forward service/user-interface-service 5003:5003 &

echo "UI is Live! Access it at: http://localhost:5003"