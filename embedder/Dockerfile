# Use a base image that supports Python
FROM python:3.9-slim

# Install required packages
RUN pip install --no-cache-dir langchain watchdog psycopg2-binary sentence-transformers 

# Create necessary directories
RUN mkdir -p /pages /usr/local/models

# Set the working directory to where the volume will mount
WORKDIR /app


# Copy the monitoring script to the container
#COPY monitor.py /usr/local/bin/monitor.py

#TODO make models local
COPY models /usr/local/models
# Make the script executable
#RUN chmod +x /usr/local/bin/monitor.py

# Ensure line endings are correct
RUN apt-get update && apt-get install -y dos2unix
#RUN dos2unix /usr/local/bin/monitor.py

# Set the entry point to run the monitor script
ENTRYPOINT ["python", "monitor.py"]

