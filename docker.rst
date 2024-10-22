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
this container waits for an incoming file in the dockervolume : and then converts pdf to txt

embedder:
---------
this container chops the txt-file and inserts into a postgres database

postgres:
---------
this a combination of management and a vectordatabase
(contains the script to create the 'document_chunks' table


where to find docker containers
-------------------------------
in the directories:
- pdfconverter2
- postgres
- embedder

are Dockerfiles
- use docker build -t pdfconverter . (for building)
....

compose
-------
there are docker-compose.yml files in :
- postgres
- rag

The one in postgres : 
- creates 2 containers  (database + management)
- inits the postgres database as a vectordatabase and creates a table 

The one in rag : 
- creates a volume where you can copy pdf files
- creates a volume where converted text files are stored 
- defines environment variables to access the database (to be changed on your environment!)
*docker compose up -d*

copy pdf files to the container
-------------------------------
cp 270123.pdf /var/snap/docker/common/var-lib-docker/volumes/rag_leech_data/_data
