# Dockerfile

# Start with a base Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8502

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]

