# Use an official Python runtime as the base image
FROM python:3.9-slim

# Optional
RUN apt-get update && apt-get install -y \
    fortune \
    cowsay \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code into the container
COPY src/main.py .

# Run the bot when the container launches
CMD ["python", "main.py"]