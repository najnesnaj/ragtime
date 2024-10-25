# Dockerfile for the Flask web frontend
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code
COPY app /app

# Copy templates and static folders
COPY templates /app/templates
COPY static /app/static

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]



