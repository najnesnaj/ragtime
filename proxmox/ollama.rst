ollama install and use
======================
curl -fsSL https://ollama.com/install.sh | sh


using a container
-----------------

ollama-model-gemma2 was mounted using a volume and the image exported 

sudo docker import ollama.tar ollama:latest
