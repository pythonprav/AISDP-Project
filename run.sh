#!/bin/bash

# Define Variables
PREPROCESS_IMAGE="pengpengintotheroom/preprocess"
PREPROCESS_CONTAINER="data-preprocessing-container"
TRAIN_IMAGE="pravallikadocker123/model-training"
TRAIN_CONTAINER="model-training-container"
IMAGE_TAG="latest"
HOST="localhost"
PREPROCESS_PORT="5000"
TRAIN_PORT="5001"
TRAIN_ENDPOINT="train"
PREPROCESS_ENDPOINT="preprocess"

echo "====================================="
echo "🚀 STEP 1: Building Data Preprocessing Docker Image..."
echo "====================================="
docker build -t $PREPROCESS_IMAGE:$IMAGE_TAG -f data-preprocessing/data_preprocessing.dockerfile .

if [ $? -eq 0 ]; then
    echo "✅ Data Preprocessing Image built successfully: $PREPROCESS_IMAGE:$IMAGE_TAG"
else
    echo "❌ Data Preprocessing build failed!"
    exit 1
fi

echo ""
echo "====================================="
echo "🚀 STEP 2: Running Data Preprocessing Container..."
echo "====================================="
docker run -d --name $PREPROCESS_CONTAINER \
  -p 5000:5000 \
  -v "$(pwd)/volumes/data:/volumes/data" \
  -v "$(pwd)/volumes/user:/volumes/user" \
  $PREPROCESS_IMAGE:$IMAGE_TAG

if [ $? -eq 0 ]; then
    echo "✅ Data Preprocessing Container started: $PREPROCESS_CONTAINER"
else
    echo "❌ Failed to start Data Preprocessing Container!"
    exit 1
fi

echo ""
echo "====================================="
echo "🚀 STEP 3: Sending Preprocessing Request..."
echo "====================================="
curl -X POST http://$HOST:$PREPROCESS_PORT/$PREPROCESS_ENDPOINT

if [ $? -eq 0 ]; then
    echo "✅ Data Preprocessing completed successfully!"
else
    echo "❌ Data Preprocessing failed!"
    exit 1
fi

echo ""
echo "====================================="
echo "🚀 STEP 4: Building Model Training Docker Image..."
echo "====================================="
docker build -t $TRAIN_IMAGE:$IMAGE_TAG -f model-training/model_training.dockerfile .

if [ $? -eq 0 ]; then
    echo "✅ Model Training Image built successfully: $TRAIN_IMAGE:$IMAGE_TAG"
else
    echo "❌ Model Training build failed!"
    exit 1
fi

echo ""
echo "====================================="
echo "🚀 STEP 5: Running Model Training Container..."
echo "====================================="
docker run -d --name $TRAIN_CONTAINER \
  -p 5001:5001 \
  -v "$(pwd)/volumes/data:/volumes/data" \
  -v "$(pwd)/volumes/models:/volumes/models" \
  $TRAIN_IMAGE:$IMAGE_TAG

if [ $? -eq 0 ]; then
    echo "✅ Model Training Container started: $TRAIN_CONTAINER"
else
    echo "❌ Failed to start Model Training Container!"
    exit 1
fi

echo ""
echo "====================================="
echo "🚀 STEP 6: Deploying to Kubernetes..."
echo "====================================="
kubectl apply -f data-preprocessing/preprocess_deployment.yaml
kubectl apply -f model-training/model-training-deployment.yaml

if [ $? -eq 0 ]; then
    echo "✅ Kubernetes deployments applied!"
else
    echo "❌ Kubernetes deployment failed!"
    exit 1
fi

echo ""
echo "====================================="
echo "🚀 STEP 7: Waiting for Containers to Be Ready..."
echo "====================================="
sleep 10  # Wait for containers to fully start

echo ""
echo "====================================="
echo "🚀 STEP 8: Sending Model Training Request..."
echo "====================================="
curl -X POST http://$HOST:$TRAIN_PORT/$TRAIN_ENDPOINT

if [ $? -eq 0 ]; then
    echo "✅ Model Training started successfully!"
else
    echo "❌ Model Training request failed!"
    exit 1
fi

echo ""
echo "====================================="
echo "🚀 STEP 9: Fetching Logs..."
echo "====================================="
echo "📜 Data Preprocessing Logs:"
docker logs -f $PREPROCESS_CONTAINER &

echo "📜 Model Training Logs:"
docker logs -f $TRAIN_CONTAINER


echo ""
echo "====================================="
echo "🚀 STEP 10: Building Model Inference Docker Image..."
echo "====================================="
docker build -t $INFERENCE_IMAGE:$IMAGE_TAG -f model-inference/model_inference.dockerfile .

if [ $? -eq 0 ]; then
    echo "✅ Model Inference Image built successfully: $INFERENCE_IMAGE:$IMAGE_TAG"
else
    echo "❌ Model Inference build failed!"
    exit 1
fi

echo ""
echo "====================================="
echo "🚀 STEP 11: Running Model Inference Container..."
echo "====================================="
docker run -d --name $INFERENCE_CONTAINER \
  -p 5002:5002 \
  -v "$(pwd)/volumes/data:/volumes/data" \
  -v "$(pwd)/volumes/models:/volumes/models" \
  -v "$(pwd)/volumes/user:/volumes/user" \
  $INFERENCE_IMAGE:$IMAGE_TAG

if [ $? -eq 0 ]; then
    echo "✅ Model Inference Container started: $INFERENCE_CONTAINER"
else
    echo "❌ Failed to start Model Inference Container!"
    exit 1
fi

echo ""
echo "====================================="
echo "🚀 STEP 12: Deploying Inference Service to Kubernetes..."
echo "====================================="
kubectl apply -f model-inference/model-inference-deployment.yaml

if [ $? -eq 0 ]; then
    echo "✅ Model Inference deployed to Kubernetes!"
else
    echo "❌ Model Inference deployment failed!"
    exit 1
fi

echo ""
echo "====================================="
echo "🚀 STEP 13: Sending Prediction Request..."
echo "====================================="
curl -X POST http://$HOST:$INFERENCE_PORT/$INFERENCE_ENDPOINT

if [ $? -eq 0 ]; then
    echo "✅ Model Inference completed successfully!"
else
    echo "❌ Model Inference request failed!"
    exit 1
fi

echo ""
echo "====================================="
echo "🚀 STEP 14: Fetching Inference Logs..."
echo "====================================="
docker logs -f $INFERENCE_CONTAINER