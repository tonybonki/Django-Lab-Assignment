import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import subprocess

class FolderCreationHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            print(f"Folder created: {event.src_path}")
            # Run your copying script here

if __name__ == "__main__":
    target_directory = os.getcwd()  # Directory to monitor

    event_handler = FolderCreationHandler()
    observer = Observer()
    observer.schedule(event_handler, path=target_directory, recursive=False)

    print(f"Monitoring directory: {target_directory}")

    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the script you want to run (in this case, it's the same script)
    script_to_run = os.path.join(current_directory, 'move_to_react.py')

    # Run the script using subprocess
    subprocess.run(['python', script_to_run], check=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()