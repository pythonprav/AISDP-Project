# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only necessary files
<<<<<<< Updated upstream
COPY model-inference/requirements.txt ./  
COPY model-inference/inference.py ./  
=======
COPY requirements.txt ./
#Only copying inference-related code
COPY inference.py ./  
>>>>>>> Stashed changes

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 5002

# Run the inference application
<<<<<<< Updated upstream
CMD ["python", "./inference.py"]

=======
CMD ["python", "inference.py"]
>>>>>>> Stashed changes


# Use an official Python runtime as the base image
# FROM python:3.9-slim

# # Set the working directory inside the container
# WORKDIR /app

# # Copy the entire data-preprocessing folder (including data and scripts)
# COPY . /app/

# # Ensure the 'data' directory exists
# RUN mkdir -p /app/data

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose the Flask app port
# EXPOSE 5000

# # Run the preprocessing application
<<<<<<< Updated upstream
# CMD ["python", "preprocess.py"]
# # Run the preprocessing application
=======
>>>>>>> Stashed changes
# CMD ["python", "preprocess.py"]