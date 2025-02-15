# Base image: Python 3.9 slim
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY ./user-interface/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install docker.io for Docker commands
RUN apt-get update && \
    apt-get install -y docker.io curl && \
    apt-get clean

# Install kubectl for Kubernetes commands inside container
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/kubectl && \
    apt-get clean

# Copy application files
COPY ./user-interface/ .

# Expose port for Flask app
EXPOSE 5003

# Run the Flask application
CMD ["python3", "winequality_app.py"]