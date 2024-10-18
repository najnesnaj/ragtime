#!/usr/bin/env python3
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import subprocess

class LeechHandler(FileSystemEventHandler):
    def __init__(self, leech_dir, pages_dir):
        self.leech_dir = leech_dir
        self.pages_dir = pages_dir

    def on_created(self, event):
        if event.is_directory:
            return None
        elif event.src_path.endswith(".pdf"):
            print(f"New PDF detected: {event.src_path}")
            subprocess.run(["python", "/usr/local/bin/convert.py"])

if __name__ == "__main__":
    leech_dir = "/leech"
    pages_dir = "/pages"
    
    event_handler = LeechHandler(leech_dir, pages_dir)
    observer = Observer()
    observer.schedule(event_handler, path=leech_dir, recursive=False)
    
    print(f"Watching {leech_dir} for new PDF files...")
    
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

