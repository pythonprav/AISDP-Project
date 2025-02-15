# Use Python 3.9 (same as preprocessing)
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code to the container
COPY . .

# Create necessary directories
RUN mkdir -p /app/volumes/data /app/volumes/models

# Set the command to run the training script
CMD ["python", "train_model.py"]