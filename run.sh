#!/bin/bash

# 🚀 Set Variables
DOCKER_USERNAME="myrepo"  # Change this to your Docker Hub username
K8S_NAMESPACE="default"   # Change if using a different namespace

echo "🚀 Starting Deployment Process..."

# ✅ Step 1: Build Docker Images
echo "🔨 Building Docker Images..."
docker build -t $DOCKER_USERNAME/webapp:latest ./user-interface
docker build -t $DOCKER_USERNAME/data-preprocessing:latest ./data-preprocessing
docker build -t $DOCKER_USERNAME/model-training:latest ./model-training
docker build -t $DOCKER_USERNAME/model-inference:latest ./model-inference

# ✅ Step 2: Push Images to Docker Hub
echo "📤 Pushing Docker Images..."
docker push $DOCKER_USERNAME/webapp:latest
docker push $DOCKER_USERNAME/data-preprocessing:latest
docker push $DOCKER_USERNAME/model-training:latest
docker push $DOCKER_USERNAME/model-inference:latest

# ✅ Step 3: Apply Persistent Storage
echo "💾 Applying Persistent Volumes..."
kubectl apply -f pv.yml

# ✅ Step 4: Deploy Application
echo "🚀 Deploying Kubernetes Services..."
kubectl apply -f deployment.yml

# ✅ Step 5: Expose Web App
echo "🌍 Exposing Web Application..."
kubectl apply -f service.yml

# ✅ Step 6: Verify Deployments
echo "🔎 Verifying Deployments..."
kubectl get pods -n $K8S_NAMESPACE
kubectl get services -n $K8S_NAMESPACE

# ✅ Step 7: Get Web App URL
echo "🌐 Access Web App:"
kubectl get svc webapp-service -n $K8S_NAMESPACE

echo "✅ Deployment Completed Successfully! 🚀"
