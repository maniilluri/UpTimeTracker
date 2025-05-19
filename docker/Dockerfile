# Use a lightweight Python image
FROM python:3.10-slim
ENV prometheus_multiproc_dir=/tmp/metrics


# Set the working directory inside the container
WORKDIR /app

# Copy necessary files
COPY monitor/ monitor/
COPY metrics/ metrics/
COPY requirements.txt ./


# Unbuffered output so logs print immediately
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app 


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Creates the logs/ directory inside /app, so that: with open("logs/health.log", "a") wont crash. 
RUN mkdir -p logs


# Set the default command to run your health checker
CMD ["python", "monitor/checker.py"]


