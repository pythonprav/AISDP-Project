# chmod +x docker_run.sh
# ./docker_run.sh

echo "Stopping and removing any existing containers..."
docker stop data-preprocessing model-training model-inference user-interface 2>/dev/null
docker rm data-preprocessing model-training model-inference user-interface 2>/dev/null

echo "Removing existing Docker network (if any)..."
docker network rm wine-net 2>/dev/null

echo "Creating Docker network: wine-net..."
docker network create wine-net

# Data Preprocessing Container
echo "Building data-preprocessing container..."
docker build -t pariikubavat/data-preprocessing:latest -f data-preprocessing/data_preprocessing.dockerfile data-preprocessing/

echo "Running data-preprocessing container..."
docker run -d --name data-preprocessing \
  --network wine-net \
  -p 5004:5004 \
  -v "$(pwd)/volumes/data:/app/volumes/data" \
  -v "$(pwd)/volumes/user:/app/volumes/user" \
  pariikubavat/data-preprocessing:latest

sleep 5  # Wait for preprocessing to complete

# Model Training Container
echo "🔧 Building model-training container..."
docker build -t pariikubavat/model-training:latest -f model-training/model_training.dockerfile model-training/

echo "Running model-training container..."
docker run --rm --name model-training \
  --network wine-net \
  -v "$(pwd)/volumes/data:/app/volumes/data" \
  -v "$(pwd)/volumes/models:/app/volumes/models" \
  pariikubavat/model-training:latest

sleep 5  # Ensure the model file is saved

# Model Inference Container
echo "🔧 Building model-inference container..."
docker build -t pariikubavat/model-inference:latest -f model-inference/model_inference.dockerfile model-inference/

echo "Running model-inference container..."
docker run -d --name model-inference \
  --network wine-net \
  -p 5001:5001 \
  -v "$(pwd)/volumes/models:/app/volumes/models" \
  -v "$(pwd)/volumes/user:/app/volumes/user" \
  pariikubavat/model-inference:latest

sleep 5  # Give it time to start

# User Interface Container
echo "🔧 Building user-interface container..."
docker build -t pariikubavat/user-interface:latest -f user-interface/web_application.dockerfile user-interface/

echo "Running user-interface container..."
docker run -d --name user-interface \
  --network wine-net \
  -p 5003:5003 \
  -v "$(pwd)/volumes/user:/app/volumes/user" \
  pariikubavat/user-interface:latest

echo "All containers are running!"
echo " --> Access the UI at: http://localhost:5003"