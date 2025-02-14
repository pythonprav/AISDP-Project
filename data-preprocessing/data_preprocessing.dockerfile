# Base Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY data-preprocessing/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary preprocessing files
COPY data-preprocessing/preprocess.py ./  
COPY data-preprocessing/preprocess_deployment.yaml ./  
COPY data-preprocessing/pv-pvc.yaml ./  

# Expose Flask port
EXPOSE 5000

# Run the preprocessing application
CMD ["python", "./preprocess.py"]


# old codes
# Base Image
# FROM python:3.9-slim

# # Set working directory
# WORKDIR /app

# # Copy requirements and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the entire preprocessing folder
# COPY . .

# # Ensure volumes/data directory exists
# RUN mkdir -p /app/volumes/data /app/volumes/user

# # Expose Flask port
# EXPOSE 5000

# # Run the preprocessing application
# CMD ["python", "./preprocess.py"]