#!/bin/bash

echo "🚀 Stopping and Removing Existing Containers..."
docker stop user-interface model-inference model-training data-preprocessing 2>/dev/null
docker rm user-interface model-inference model-training data-preprocessing 2>/dev/null
docker network rm wine-net 2>/dev/null

echo "🔗 Creating Docker Network..."
docker network create wine-net

echo "🛠️ Building and Running Data Preprocessing Container..."
cd data-preprocessing
docker build -t pariikubavat/data-preprocessing:latest -f data_preprocessing.dockerfile .
docker run -d --name data-preprocessing \
  --network wine-net \
  -p 5000:5000 \
  -e RAW_DATA_DIR="/app/raw_data" \
  -e OUTPUT_DIR="/app/volumes/data" \
  -e USER_INPUTS_DIR="/app/volumes/user" \
  -v "$(pwd)/raw_data:/app/raw_data" \
  -v "$(pwd)/../volumes/data:/app/volumes/data" \
  -v "$(pwd)/../volumes/user:/app/volumes/user" \
  pariikubavat/data-preprocessing:latest
cd ..

echo "⌛ Waiting for Data Preprocessing to complete..."
sleep 5  # Give it some time to process the initial dataset

echo "🛠️ Building and Running Model Training Container..."
cd model-training
docker build -t pariikubavat/model-training:latest -f model_training.dockerfile .
docker run --name model-training \
  --network wine-net \
  -e DATA_PATH="/app/volumes/data/cleaned_wine_quality.csv" \
  -e MODEL_PATH="/app/volumes/models/saved_model.pkl" \
  -v "$(pwd)/../volumes/data:/app/volumes/data" \
  -v "$(pwd)/../volumes/models:/app/volumes/models" \
  pariikubavat/model-training:latest
cd ..

echo "🛠️ Building and Running Model Inference Container..."
cd model-inference
docker build -t pariikubavat/model-inference:latest -f model_inference.dockerfile .
docker run -d --name model-inference \
  --network wine-net \
  -e MODEL_PATH="/app/volumes/models/saved_model.pkl" \
  -e INPUT_PATH="/app/volumes/user/cleaned_input.csv" \
  -e OUTPUT_PATH="/app/volumes/user/predictions.json" \
  -v "$(pwd)/../volumes/models:/app/volumes/models" \
  -v "$(pwd)/../volumes/user:/app/volumes/user" \
  -p 5001:5001 \
  pariikubavat/model-inference:latest
cd ..

echo "🛠️ Building and Running User Interface Container..."
cd user-interface
docker build -t pariikubavat/user-interface:latest -f web_application.dockerfile .
docker run -d --name user-interface \
  --network wine-net \
  -e USER_DIR="/app/volumes/user" \
  -e INFERENCE_API="http://model-inference:5001/predict" \
  -v "$(pwd)/../volumes/user:/app/volumes/user" \
  -p 5003:5003 \
  pariikubavat/user-interface:latest
cd ..

echo "✅ All containers are running successfully!"

echo "🌐 Access the User Interface at: http://localhost:5003"
echo "🔍 Check the Data Preprocessing API at: http://localhost:5000/get-data"
echo "🔍 Check the Inference API at: http://localhost:5001/predict"