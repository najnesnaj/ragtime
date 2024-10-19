install something from docker
=============================
  https://docs.docker.com/engine/install/ubuntu/
  https://download.docker.com/linux/ubuntu/dists/jammy/pool/stable/amd64/

using portainer:
----------------

  sudo docker volume create portainer_data
  sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:2.21.3

using github to build containers:
---------------------------------

see github actions (and actions.rst in the doc)


leecher:
-------
custommade : pdf copy to directory leech


building pdf to text:
---------------------

docker build -t pdf-text-converter .
docker run -v $(pwd)/leech:/app/leech -v $(pwd)/pages:/app/pages pdf-text-converter


pdfconverter2
--------------------------------------
docker build -t pdf-watcher .
docker run -v ($pwd)/leech:/leech -v ($pwd)/pages:/pages pdf-watcher


