# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install kubectl
RUN apt-get update && apt-get install -y curl && \
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/

# Install dependencies
COPY ./model-inference/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files
COPY ./model-inference/ .

# Expose port for model-inference
EXPOSE 5001

# Run the model inference
ENTRYPOINT ["python3"]
CMD ["inference.py"]