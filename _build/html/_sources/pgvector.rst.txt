storing vector + metadata
=========================


PostgreSQL + pgvector Example
If you prefer using PostgreSQL, you can use the pgvector extension, which allows you to store vector embeddings in a PostgreSQL table alongside metadata.

Steps:

- Install pgvector: First, install the pgvector extension.
- Create a table: Create a table that stores both vectors and metadata.
- Insert vectors and metadata: Insert each chunk’s vector along with its metadata.
sql
