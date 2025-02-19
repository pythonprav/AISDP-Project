#!/bin/bash

echo "Starting User Interface Deployment"

echo "Freeing Port 5003..."
fuser -k 5003/tcp 2>/dev/null || true  # Kills process using port 5003 (ignores error if none found)

echo "Deploying UI..."
kubectl delete deployment user-interface --ignore-not-found
kubectl delete service user-interface-service --ignore-not-found

echo "Building and Pushing UI Docker Image..."
cd user-interface
docker build -t pariikubavat/user-interface:latest -f web_application.dockerfile .
docker push pariikubavat/user-interface:latest
cd ..

echo "Applying Kubernetes Deployment and Service..."
kubectl apply -f k8s/user-interface-deployment.yaml
kubectl apply -f k8s/user-interface-service.yaml

echo "Waiting for UI pod to be ready..."
kubectl wait --for=condition=ready pod -l app=user-interface --timeout=120s

echo "Port Forwarding UI to localhost:5003"
kubectl port-forward service/user-interface-service 5003:5003 &

echo "UI is Live! Access it at: http://localhost:5003"