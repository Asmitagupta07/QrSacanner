import os
import threading
import webview

# Start the Django server
def start_django_server():
    os.system("python manage.py runserver 127.0.0.1:8000")

# Launch the desktop application
if __name__ == "__main__":
    # Run Django server in a separate thread
    threading.Thread(target=start_django_server, daemon=True).start()
    
    # Create a web view window pointing to the local Django server
    webview.create_window("My Django Desktop App", "http://127.0.0.1:8000")
    webview.start()
