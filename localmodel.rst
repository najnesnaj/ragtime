Preventing Model Downloads in Docker Containers
===============================================

When using the `paraphrase-multilingual-mpnet-base-v2` model in Python, the script may download the model from Hugging Face each time it is executed. This can cause repeated downloads when running the script inside a Docker container. To prevent this, you can pre-download the model and include it in your Docker image.

Steps to Pre-download and Embed the Model
-----------------------------------------

1. **Modify the Dockerfile to Pre-download the Model**

   Update your `Dockerfile` to download the model during the image build process. This ensures the model is cached in the container.

   Example Dockerfile:

   .. code-block:: dockerfile

      FROM python:3.9-slim

      # Install necessary dependencies
      RUN pip install --no-cache-dir torch transformers sentence-transformers

      # Pre-download the model
      RUN python -c "from transformers import AutoTokenizer, AutoModel; \
          AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-multilingual-mpnet-base-v2'); \
          AutoModel.from_pretrained('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')"

      # Copy your application code into the container
      COPY . /app
      WORKDIR /app

      # Set the command to run your script
      CMD ["python", "your_script.py"]

2. **Optional: Set a Custom Cache Directory**

   If you want to use a specific directory for caching the model, you can set the `HF_HOME` environment variable in the Dockerfile.

   Example:

   .. code-block:: dockerfile

      ENV HF_HOME=/app/cache/huggingface
      RUN mkdir -p $HF_HOME
      RUN python -c "from transformers import AutoTokenizer, AutoModel; \
          AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-multilingual-mpnet-base-v2'); \
          AutoModel.from_pretrained('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')"

3. **Build and Run the Docker Image**

   Build the Docker image with the following command:

   .. code-block:: bash

      docker build -t my-docker-app .

   Then, run the container:

   .. code-block:: bash

      docker run --rm -it my-docker-app

4. **Verify the Model is Cached**

   You can verify that the model is included in the container by checking the cache directory:

   .. code-block:: bash

      docker run --rm -it my-docker-app bash
      ls ~/.cache/huggingface/transformers  # Or the custom cache directory

Advantages
----------

- **Faster Start-up Time:** The container does not need to download the model at runtime.
- **No Internet Dependency:** The container can run without internet access after the image is built.

Considerations
--------------

- **Increased Image Size:** Pre-downloading the model increases the Docker image size. Use tools like `docker-slim` to optimize the image if necessary.
- **Updates:** To update the model, you must rebuild the Docker image with the updated version.

This approach ensures that your Docker container can execute the script efficiently without repeated downloads of the model.

