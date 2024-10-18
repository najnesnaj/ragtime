# Use a base image that supports Python and your conversion tool (PyMuPDF in this case)
FROM python:3.9-slim

# Install required packages
RUN pip install PyMuPDF watchdog

# Create necessary directories
RUN mkdir -p /leech /pages

# Copy your conversion script to the container
COPY convert.py /usr/local/bin/convert.py

# Make the script executable
RUN chmod +x /usr/local/bin/convert.py

# Set up a script to continuously check the leech directory
COPY watch.py /usr/local/bin/watch.py
RUN chmod +x /usr/local/bin/watch.py

# Set the entry point to run the watcher script
ENTRYPOINT ["/usr/local/bin/watch.py"]

