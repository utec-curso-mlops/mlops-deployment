# Use an official Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Evidently
#RUN pip install --no-cache-dir evidently==0.6.7
RUN pip install --no-cache-dir evidently==0.7.8

ENTRYPOINT ["evidently", "ui", "--host", "0.0.0.0"]