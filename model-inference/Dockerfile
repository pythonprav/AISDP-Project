# Use Python 3.9 as the base image
FROM python:3.9

# Define a build-time argument for Docker Hub username
ARG DOCKER_USERNAME
ENV DOCKER_USERNAME=${DOCKER_USERNAME}

# Set the working directory inside the container
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the API port
EXPOSE 5002

# Run the inference script
CMD ["python", "inference.py"]