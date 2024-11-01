# ragtime
RAG LLM docker ollama pgvector

the purpose of this project is to enhance the retrieval of information in documents:
- add metadata1 based on the content
- add metadata2 based on the type of document

explanation:
------------

suppose documents contain both a problem and the solution.
Some problems will be similar, so in metadata1 we put the problemcategory.
Within the text, we use metadata2 to describe weather its a solution or a problem.


Retrieval:
----------
suppose we look for solutions for a particular problem:
- determine the problemcategory for our search
- search for similar problems(vectorise the particular problem) in the vectordatabase for that problemcategory only

(this will limit full search already)

- in formulating a respons (the others problems are not relevant), hence metadata2 which describes the section of the document

(this will avoid feeding extra text to a LLM)  


experimenting with retrieval augmented generation
-------------------------------------------------  

setup docker services that : 

- convert pdf to text
- embed text into pgvector (postgres)
- add metadata
- retrieve

https://ragtime.readthedocs.io/en/latest/


docker containers
-----------------
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
cp 270123.pdf /var/lib/docker/volumes/rag_leech_data/_data 
