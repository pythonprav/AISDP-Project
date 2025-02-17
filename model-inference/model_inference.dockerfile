# Use Python 3.9 (same as other containers)
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose port for the API
EXPOSE 5001

# Run the model inference
CMD ["python3", "inference.py"]