# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV STORAGE_TYPE aws

# Set the working directory in the container
WORKDIR /home

# Copy the requirements file into the container
COPY requirements.txt /home/app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /home/app/requirements.txt

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install AWS cli
RUN pip3 --no-cache-dir install --upgrade awscli

# Move AWS Credentials and config
COPY credentials /home/.aws/
COPY config /home/.aws/

# Set Env var for AWS cli
ENV AWS_SHARED_CREDENTIALS_FILE=/home/.aws/credentials
ENV AWS_CONFIG_FILE=/home/.aws/config

# Copy the rest of the application code into the container
COPY app/ /home/app/

# Expose the port the FastAPI application will run on
EXPOSE 8000

# Define the command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
