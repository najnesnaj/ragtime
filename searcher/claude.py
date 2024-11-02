import os
import numpy as np
import psycopg2
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Any

class VectorDatabase:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize the vector database with the specified embedding model."""
        self.model = SentenceTransformer(model_name)
        self.connection = None
        
    def create_connection(self) -> None:
        """Create a connection to PostgreSQL database."""
        self.connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

    def setup_database(self) -> None:
        """Set up the database schema with proper vector data type."""
        self.create_connection()
        with self.connection.cursor() as cursor:
            # Create extension if it doesn't exist
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            
            # Create table with vector data type
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS document_chunks (
                    id SERIAL PRIMARY KEY,
                    document_id TEXT,
                    chunk_id INTEGER,
                    meta_data1 TEXT,
                    meta_data2 TEXT,
                    text TEXT,
                    section TEXT,
                    embedding vector(384)
                );
            """)
            
            # Create an index for faster similarity search
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS embedding_idx 
                ON document_chunks 
                USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100);
            """)
            
            self.connection.commit()

    def insert_document(self, 
                       text: str, 
                       document_id: str, 
                       chunk_id: int, 
                       meta_data1: str, 
                       meta_data2: str, 
                       section: str) -> None:
        """Insert a document with its embedding into the database."""
        # Generate embedding
        embedding = self.model.encode(text)
        
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO document_chunks 
                (document_id, chunk_id, meta_data1, meta_data2, text, section, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (document_id, chunk_id, meta_data1, meta_data2, text, section, embedding.tolist()))
            
        self.connection.commit()

    def get_top_matches(self, query: str, limit: int = 10) -> List[Tuple[Any, float]]:
        """
        Retrieve top matches using vector similarity search.
        
        Args:
            query: The search query string
            limit: Maximum number of results to return
            
        Returns:
            List of tuples containing (row_data, similarity_score)
        """
        # Generate query embedding
        query_embedding = self.model.encode(query)
        
        with self.connection.cursor() as cursor:
            # Use PostgreSQL's vector similarity search
            cursor.execute("""
                SELECT id, document_id, chunk_id, meta_data1, meta_data2, text, section, 
                       embedding, 1 - (embedding <=> %s) as similarity
                FROM document_chunks
                ORDER BY embedding <=> %s
                LIMIT %s;
            """, (query_embedding.tolist(), query_embedding.tolist(), limit))
            
            results = cursor.fetchall()
            
        return [(row[:-2], row[-1]) for row in results]  # Exclude embedding and return similarity

    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()

# Example usage
def main():
    # Initialize the vector database
    db = VectorDatabase()
    
    # Set up the database schema
    db.setup_database()
    
    # Example: Insert a document
    db.insert_document(
        text="Example document text",
        document_id="doc1",
        chunk_id=1,
        meta_data1="meta1",
        meta_data2="meta2",
        section="section1"
    )
    
    # Example: Perform similarity search
    results = db.get_top_matches("similar text")
    
    for row_data, similarity in results:
        print(f"Similarity: {similarity:.4f}")
        print(f"Document ID: {row_data[1]}")
        print(f"Text: {row_data[5]}")
        print("---")
    
    # Close the connection
    db.close()

if __name__ == "__main__":
    main()
