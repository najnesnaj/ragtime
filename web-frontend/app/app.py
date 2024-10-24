import os
from flask import Flask, request, render_template, jsonify
import psycopg2
import requests
from transformers import AutoTokenizer, AutoModel
import torch

app = Flask(__name__)

# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Connect to PostgreSQL using environment variables
def connect_db():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        dbname=os.getenv("POSTGRES_DB", "vector_db"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password")
    )
    return conn

# Generate embeddings using AutoTokenizer and AutoModel
def generate_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings.numpy()

# Search the vector database
def search_vector(query_embedding):
    conn = connect_db()
    cur = conn.cursor()

    # Example query using pgvector similarity function
    cur.execute("""
        SELECT text_chunk, metadata 
        FROM your_table 
        ORDER BY embedding <-> %s 
        LIMIT 5;
    """, (query_embedding,))
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    
    # Generate embedding for the query
    query_embedding = generate_embeddings([query])

    # Search the PostgreSQL vector table
    results = search_vector(query_embedding.tolist()[0])
    
    # Send results to LLM for summarization/response formulation
    response = call_llm_service(results)
    
    return jsonify({"response": response})

def call_llm_service(results):
    llm_api_url = os.getenv("LLM_API_URL", "http://llm_container:5000/generate")
    
    payload = {
        "chunks": [result[0] for result in results]
    }
    
    response = requests.post(llm_api_url, json=payload)
    return response.json()["generated_text"]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

