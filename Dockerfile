# FROM python:3.9-slim
# WORKDIR /app

# # Copy the requirements file to the container
# COPY requirements.in .

# # Install the Python dependencies
# RUN pip install --no-cache-dir -r requirements.in

# # Copy the rest of the application code to the container
# COPY . .

# # Expose the default Streamlit port
# EXPOSE 8501

# # Set the entry point for the container
# ENTRYPOINT ["streamlit", "run"]
# CMD ["app.py"]

# Use the official CUDA base image
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    curl

# Install CUDA-enabled version of Python
RUN pip3 install --no-cache-dir --upgrade pip

# Copy the requirements file to the container
COPY requirements.in .

# Install the Python dependencies
RUN pip3 install --no-cache-dir -r requirements.in

# Copy the rest of the application code to the container
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Set the entry point for the container
ENTRYPOINT ["streamlit", "run"]

# Set the default command to run your Streamlit application
CMD ["app.py"]
