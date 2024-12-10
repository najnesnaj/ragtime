# Use a base image that supports Python
FROM python:3.9-slim
#RUN apt-get update && apt-get install -y libpq-dev

# Install required packages
RUN pip install --no-cache-dir watchdog psycopg2-binary sentence-transformers


# Download the model during the build
RUN python -c "from transformers import AutoTokenizer, AutoModel; \
               AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2'); \
               AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')"



# Create necessary directories
RUN mkdir -p /pages

# Copy the monitoring script to the container
COPY monitor.py /usr/local/bin/monitor.py

#TODO make models local
#COPY models /usr/local/models
# Make the script executable
RUN chmod +x /usr/local/bin/monitor.py

# Ensure line endings are correct
RUN apt-get update && apt-get install -y dos2unix
RUN dos2unix /usr/local/bin/monitor.py

# Set the entry point to run the monitor script
ENTRYPOINT ["python", "/usr/local/bin/monitor.py"]

