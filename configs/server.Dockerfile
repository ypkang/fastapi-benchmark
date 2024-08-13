# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if any)
# RUN apt-get update && apt-get install -y git vim procps wget

# Install dependencies specified in requirements.txt (if any)
ADD src/requirements.txt .
RUN pip install --no-cache-dir --ignore-installed -r requirements.txt

# Install jaseci locally
# Remember to comment jaclang-jaseci from requirements.txt
# COPY jaclang-jaseci/ /jaclang-jaseci
# WORKDIR /jaclang-jaseci
# RUN pip install -e .
# WORKDIR /app

# Copy the current directory contents into the container at /app
ADD start.sh /app
ADD restart.sh /app
ADD src/ /app

# Make port 5000 available to the world outside this container
EXPOSE 8000

# Define environment variable