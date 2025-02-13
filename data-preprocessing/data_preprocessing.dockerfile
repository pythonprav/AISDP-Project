# Base Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire preprocessing folder
COPY . .

# Ensure volumes/data directory exists
RUN mkdir -p /app/volumes/data /app/volumes/user

# Expose Flask port
EXPOSE 5000

# Run the preprocessing application
CMD ["python", "preprocess.py"]