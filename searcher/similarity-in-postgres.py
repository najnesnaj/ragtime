import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect("dbname=your_db user=your_user password=your_password host=localhost")
cursor = conn.cursor()

# Define your query vector
query_vector = model.encode("your query text here").tolist()

# Convert the vector to a format suitable for SQL
query_vector_str = "ARRAY" + str(query_vector)

# Execute the similarity search SQL query
cursor.execute(f"""
    SELECT id, document_id, chunk_id, text, 
           1 - (embedding <=> {query_vector_str}) AS similarity  -- Cosine similarity
    FROM document_chunks
    ORDER BY embedding <=> {query_vector_str}
    LIMIT 10;
""")
results = cursor.fetchall()

# Close the connection
cursor.close()
conn.close()

# Display results
for result in results:
    print(result)

