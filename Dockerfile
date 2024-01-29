FROM ubuntu

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy application files
COPY . /app

# Set working directory
WORKDIR /app
