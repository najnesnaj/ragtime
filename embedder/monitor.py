import os
import time
import psycopg2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PagesHandler(FileSystemEventHandler):
    def __init__(self, db_params):
        self.db_params = db_params

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.txt'):
            print(f"New text file detected: {event.src_path}")
            self.process_file(event.src_path)

    def process_file(self, file_path):
        title = os.path.basename(file_path).replace('.txt', '')  # Use filename as title
        
        # Read the content of the text file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Connect to PostgreSQL and insert the data
        conn = psycopg2.connect(**self.db_params)
        cursor = conn.cursor()
        
        # Assuming you have a table named 'documents' with columns 'title', 'content', and 'vector'
        # You would need to adjust this query based on your database schema
        insert_query = """
            INSERT INTO documents (title, content)
            VALUES (%s, %s);
        """
        
        # Here you can add a function to convert your text to a vector if needed.
        # For now, we're inserting the title and content only.
        cursor.execute(insert_query, (title, content))
        conn.commit()
        
        cursor.close()
        conn.close()
        print(f"Inserted: {title}")

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

