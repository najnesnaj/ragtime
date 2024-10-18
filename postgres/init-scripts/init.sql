CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with a vector column and metadata columns
CREATE TABLE IF NOT EXISTS document_chunks (
    id SERIAL PRIMARY KEY,
    document_id TEXT,
    chunk_id TEXT,
    text TEXT,
    section TEXT,
    embedding VECTOR(512)  -- Storing 512-dimensional vector embeddings
);

