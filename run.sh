#!/bin/bash

set -e  # Exit script on error

# 🚀 Define Docker Hub username dynamically
DOCKER_USERNAME="rionewman"  # Change this to your Docker Hub username

echo "🚀 Starting Deployment Process..."

# ✅ Step 1: Build Docker Images
echo "🔨 Building Docker Images..."
docker build --build-arg DOCKER_USERNAME=$DOCKER_USERNAME -t $DOCKER_USERNAME/user-interface:latest -f ./user-interface/Dockerfile ./user-interface
docker build --build-arg DOCKER_USERNAME=$DOCKER_USERNAME -t $DOCKER_USERNAME/data-preprocessing:latest -f ./data-preprocessing/Dockerfile ./data-preprocessing
docker build --build-arg DOCKER_USERNAME=$DOCKER_USERNAME -t $DOCKER_USERNAME/model-training:latest -f ./model-training/Dockerfile ./model-training
docker build --build-arg DOCKER_USERNAME=$DOCKER_USERNAME -t $DOCKER_USERNAME/model-inference:latest -f ./model-inference/Dockerfile ./model-inference

# ✅ Step 2: Push Images to Docker Hub
echo "📤 Pushing Docker Images..."
docker push $DOCKER_USERNAME/user-interface:latest
docker push $DOCKER_USERNAME/data-preprocessing:latest
docker push $DOCKER_USERNAME/model-training:latest
docker push $DOCKER_USERNAME/model-inference:latest

# ✅ Step 3: Apply Persistent Storage
echo "💾 Applying Persistent Volumes..."
kubectl apply -f pv-pvc.yml

# ✅ Step 4: Deploy Application
echo "🚀 Deploying Kubernetes Services..."
kubectl apply -f deployment.yml

# ✅ Step 5: Wait for All Pods to Be Ready
echo "🔄 Waiting for all pods to be ready..."
kubectl wait --for=condition=Ready pod --all --timeout=300s

# ✅ Step 6: Verify Deployments
echo "🔎 Checking deployment status..."
kubectl get pods
kubectl get services

# ✅ Step 7: Get Web App URL
echo "🌐 Fetching Web App URL..."
WEBAPP_URL=$(minikube service webapp-service --url)

# ✅ Step 8: Display Success Message
echo "✅ Deployment Completed Successfully!"
echo "🌍 Web App is available at: $WEBAPP_URL"