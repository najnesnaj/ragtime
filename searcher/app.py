import streamlit as st
import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

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

    # Query to retrieve embeddings and metadata
    cursor.execute("SELECT id, document_id, chunk_id, meta_data1, meta_data2, text, section, embedding FROM document_chunks")
    rows = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Calculate similarity with query embedding
    embeddings = np.array([row[-1] for row in rows])  # Extract embeddings
    similarities = cosine_similarity([query_embedding], embeddings)[0]

    # Sort by similarity and select top 10
    top_indices = similarities.argsort()[-10:][::-1]  # Top 10 indices with highest similarity
    top_matches = [(rows[i], similarities[i]) for i in top_indices]

    return top_matches

# Streamlit app UI
st.title("RAG Document Search")
st.write("Enter a query to find relevant document chunks.")

query = st.text_input("Your Query:")

if query:
    # Generate embedding for the query
    query_embedding = model.encode(query)

    # Retrieve and display the top 10 matches
    st.write("Top 10 Matches:")
    matches = get_top_matches(query_embedding)
    
    for match, similarity in matches:
        st.write(f"**Document ID**: {match[1]}")
        st.write(f"**Chunk ID**: {match[2]}")
        st.write(f"**Metadata 1**: {match[3]}")
        st.write(f"**Metadata 2**: {match[4]}")
        st.write(f"**Section**: {match[6]}")
        st.write(f"**Text**: {match[5]}")
        st.write(f"**Similarity Score**: {similarity:.4f}")
        st.write("---")

