install something from docker
=============================


*the docker build that comes with the apt-install from ubuntu does not always cut the cake*

  https://docs.docker.com/engine/install/ubuntu/
  https://download.docker.com/linux/ubuntu/dists/jammy/pool/stable/amd64/

using portainer:
----------------

  sudo docker volume create portainer_data
  sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:2.21.3

using github to build containers:
---------------------------------

see github actions (and actions.rst in the doc)



Project Dockerfiles:
--------------------

the project dockerfiles are within their own directory:
- leecher
- embedder
- postgres



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

Containers
----------    

- the Dockerfiles help to build docker images
- the docker compose file help to build containers



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

how to copy pdf files to the container?
---------------------------------------
- the dockervolumes are created using the docker-compose files
- dockervolumes link a directory in docker to a directory on the filesystem

cp 270123.pdf /var/snap/docker/common/var-lib-docker/volumes/rag_leech_data/_data


using github actions to build docker containers
-----------------------------------------------

each time there is is a push toward the github repository, automatically a build of the docker images gets triggered.

I use multiple Dockerfiles, thus multiple Docker images, and I couldn't not figure out the easy-way how to build them with a single script.

So ... multiple scripts, which each build a single image. 

By default the image gets a name like this repo:main.
This can be modified!


TRICK : multiple containers with github 
=======================================

- copy docker-publish.yml to docker-publish2.yml
- change IMAGE_NAME: 'najnesnaj/embed' 

(./embedder is de directory in the repo that contains the Dockerfile)

and change : 
 # Build and push Docker image for embedder
      - name: Build and push Docker image (embedder)
        id: build-and-push-embedder
        uses: docker/build-push-action@0565240e2d4ab88bba5387d719585280857ece09 # v5.0.0
        with:
          context: ./embedder

first login to github

echo "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxzK" | docker login ghcr.io -u najnesnaj --password-stdin

Login Succeeded

now I can download the image
naj@naj-Latitude-5520:/usr/src/ragtime$ sudo docker pull ghcr.io/najnesnaj/embed:main



elasticsearch:
--------------
- sudo docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.15.3
- sudo docker run --name kibana -p 5601:5601 --link elasticsearch:elasticsearch kibana:8.15.3

Kibana has not been configured.

Go to http://0.0.0.0:5601/?code=003763 to get started.

in the elasticsearch container generate token
(bin/elasticsearch-create-enrollment-token -s kibana)
elasticsearch-users useradd test
elasticsearch-users passwd test
elasticsearch-users roles -a kibana_admin test

