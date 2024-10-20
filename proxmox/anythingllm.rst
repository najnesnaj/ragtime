install anything LLM using docker
=================================

install Node.js and Yarn
-------------------------
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

This will add the repository for Node.js 18.x (which is the current LTS version). If you want a different version (e.g., 20.x), just replace 18.x with the desired version.

sudo apt install -y nodejs

Step 3: Verify installation
---------------------------

Check the installed version of Node.js and npm:
node -v
npm -v


Install Yarn
------------

curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install yarn

Embedding
--------- 

When your embedding engine preference is native we will use the ONNX all-MiniLM-L6-v2 model built by Xenova on HuggingFace.co. This model is a quantized and WASM version of the popular all-MiniLM-L6-v2 which produces a 384-dimension vector.

bookstack
===========
https://github.com/linuxserver/docker-bookstack/pkgs/container/bookstack

https://hub.docker.com/r/solidnerd/bookstack/


