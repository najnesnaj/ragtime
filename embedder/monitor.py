import os
import time
import psycopg2
from sentence_transformers import SentenceTransformer
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from transformers import AutoTokenizer

# Initialize tokenizer (adjust according to your model)
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Define the max tokens per chunk
MAX_TOKENS = 256  # Adjust based on your model's context length

def chunk_text(text, max_tokens=MAX_TOKENS):
    # Tokenize the input text
    tokens = tokenizer.encode(text, truncation=False)

    # Split into chunks based on max tokens
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)
    
    return chunks

class PagesHandler(FileSystemEventHandler):
    def __init__(self, db_params):
        self.db_params = db_params
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # Initialize the SentenceTransformer model

    def generate_embedding(self, text):
        # Use SentenceTransformer to generate embeddings
        embedding = self.model.encode(text)
        return embedding


    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.txt'):
            print(f"New text file detected: {event.src_path}")
            self.process_file(event.src_path)

    def process_file(self, file_path):
        document_id = os.path.basename(file_path).replace('.txt', '')  # Use filename as document_id

        title = os.path.basename(file_path).replace('.txt', '')  # Use filename as title
        
        # Read the content of the text file
        with open(file_path, 'r') as f:
            content = f.read()
#TODO        
# Split content into chunks if needed (you may implement your chunking logic)
#SentenceTransformer('all-MiniLM-L6-v2'), the context length is typically much smaller compared to models like GPT.
   #     chunks = [content]  # Assuming no chunking for now
        chunks = chunk_text(content)
        # Connect to PostgreSQL and insert the data
        conn = psycopg2.connect(**self.db_params)
        cursor = conn.cursor()

        for i, chunk in enumerate(chunks):
            chunk_id = f"{document_id}_chunk_{i+1}"
            embedding = self.generate_embedding(chunk)  # Generate the 512-dimensional vector


         
        
            insert_query = """
                INSERT INTO document_chunks (document_id, chunk_id, text, section, embedding)
                VALUES (%s, %s, %s, %s, %s);
              """
          # Convert embedding to PostgreSQL's vector format (as a list or numpy array)
            embedding_array = np.array(embedding).tolist()
        # Here you can add a function to convert your text to a vector if needed.
        # For now, we're inserting the title and content only.
            cursor.execute(insert_query, (document_id, chunk_id, chunk, None, embedding_array))

        conn.commit()
        
        cursor.close()
        conn.close()
        print(f"Inserted: {document_id}")

if __name__ == "__main__":
    pages_dir = "/pages"
    
    # Database connection parameters
    db_params = {
        'dbname': os.getenv('DB_DATABASE_NAME'),
        'user': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST', 'localhost'),  # Adjust if needed
        'port': os.getenv('DB_PORT', 5432),         # Adjust if needed
    }
    
    event_handler = PagesHandler(db_params)
    observer = Observer()
    observer.schedule(event_handler, path=pages_dir, recursive=False)
    
    print(f"Watching {pages_dir} for new text files...")
    
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

