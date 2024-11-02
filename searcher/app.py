import os
import streamlit as st
import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json  # For parsing JSON-like strings

# Load the embedding model (ensure it's compatible with your 384-dimensional vectors)
model = SentenceTransformer('all-MiniLM-L6-v2')  # Ensure this matches the 384-dimensional vector

# Connect to the PostgreSQL database using environment variables
def create_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# Retrieve top 10 matches from the database based on similarity

def get_top_matches(query_embedding):
    # Connect to the database
    conn = create_connection()
    cursor = conn.cursor()

    # Convert the query embedding to a format suitable for SQL
    #TODO niet nodig -- aanpassen
    #query_vector_str = query_embedding  # Assuming query_embedding is a list
    query_vector_str = f"ARRAY{query_embedding}" 
    # Execute the similarity search SQL query
    cursor.execute(f"""
        SELECT id, document_id, chunk_id, text, 
               1 - (embedding <=> {query_vector_str}::vector) AS similarity  -- Cosine similarity
        FROM document_chunks
        ORDER BY embedding <=> {query_vector_str}::vector
        LIMIT 10;
    """)
 # Process each row in results (ensure correct unpacking)
    results = cursor.fetchall()
    for row in results:
        id, document_id, chunk_id, text, similarity = row  # Adjust number of variables if needed
    
    # Fetch the results

    # Close the database connection
    cursor.close()
    conn.close()
    
    return results




# Streamlit app UI
st.title("RAG Document Search")
st.write("Enter a query to find relevant document chunks.")

query = st.text_input("Your Query:")

if query:
    # Generate embedding for the query
    #query_embedding = model.encode(query)
    query_embedding = model.encode(query).tolist()
    # Convert the vector to a format suitable for SQL
    query_vector_str = str(query_embedding)
    # Retrieve and display the top 10 matches
    st.write("Top 10 Matches:")
    #matches = get_top_matches(query_embedding)
    matches = get_top_matches(query_vector_str)
    for match in matches:
        document_id = match[1]
        chunk_id = match[2]
#        meta_data1 = match[3]
#        meta_data2 = match[4]
#        section = match[6]
        text = match[3]
        similarity = match[-1]  # Assuming similarity is the last item in the tuple

        st.write(f"**Document ID**: {document_id}")
        st.write(f"**Chunk ID**: {chunk_id}")
#        st.write(f"**Metadata 1**: {meta_data1}")
#        st.write(f"**Metadata 2**: {meta_data2}")
#        st.write(f"**Section**: {section}")
        st.write(f"**Text**: {text}")
        st.write(f"**Similarity Score**: {similarity:.4f}")
        st.write("---")
     

