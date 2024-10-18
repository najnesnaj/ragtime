# Use a base image that supports Python
FROM python:3.9-slim

# Install required packages
RUN pip install watchdog psycopg2

# Create necessary directories
RUN mkdir -p /pages

# Copy the monitoring script to the container
COPY monitor.py /usr/local/bin/monitor.py

# Make the script executable
RUN chmod +x /usr/local/bin/monitor.py

# Ensure line endings are correct
RUN apt-get update && apt-get install -y dos2unix
RUN dos2unix /usr/local/bin/monitor.py

# Set the entry point to run the monitor script
ENTRYPOINT ["python", "/usr/local/bin/monitor.py"]

