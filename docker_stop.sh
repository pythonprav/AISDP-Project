# bash docker_stop.sh

echo "Stopping all running containers..."
docker stop data-preprocessing model-training model-inference user-interface

echo "Removing stopped containers..."
docker rm data-preprocessing model-training model-inference user-interface

echo "Removing Docker network..."
docker network rm wine-net

echo "All containers and network have been stopped and removed."