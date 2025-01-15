# import os
# import webview
# from django.core.management import execute_from_command_line

# # Function to run the Django server
# def run_django_server():
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QrSacanner.settings')  # Ensure correct project name
#     execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000', '--noreload'])  # Disable autoreload

# # Main function to launch the desktop app
# if __name__ == '__main__':
#     # Run the Django server in the main thread (no threading)
#     run_django_server()

#     # Once the server is running, create the webview window
#     webview.create_window('My Django App', 'http://127.0.0.1:8000')  
#     webview.start()  # Start the webview

# import os
# import sys
# import threading
# import webview
# from django.core.management import execute_from_command_line

# # Set the DJANGO_SETTINGS_MODULE environment variable before importing Django modules
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QrSacanner.settings')

# # Function to run the Django server
# def run_django_server():
#     from django.conf import settings 
#     if hasattr(sys, '_MEIPASS'):
#         # If running in a bundled app (PyInstaller)
#         settings.BASE_DIR = os.path.dirname(sys.executable)
#         settings.TEMPLATES[0]['DIRS'] = [os.path.join(settings.BASE_DIR, 'templates')]
#         settings.STATICFILES_DIRS = [os.path.join(settings.BASE_DIR, 'static')]
#     else:
#         # Otherwise, for development mode
#         settings.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#         # The environment variable DJANGO_SETTINGS_MODULE is already set above

#     execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:2807', '--noreload'])

# if __name__ == '__main__':
#     # Run the Django server in a separate thread (main thread runs webview)
#     run_django_server()

#     # Once the server is running, create the webview window
#     webview.create_window('My Django App', 'http://127.0.0.1:8000')
#     webview.start()  # Start the webview window

import os
import sys
import threading
import webview
from django.core.management import execute_from_command_line
from django.conf import settings

# Set the DJANGO_SETTINGS_MODULE environment variable before importing Django modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QrSacanner.settings')

# Function to run the Django server
def run_django_server():
    if hasattr(sys, '_MEIPASS'):
        # If running in a bundled app (PyInstaller)
        settings.BASE_DIR = os.path.dirname(sys.executable)
        settings.TEMPLATES[0]['DIRS'] = [os.path.join(settings.BASE_DIR, 'templates')]
        settings.STATICFILES_DIRS = [os.path.join(settings.BASE_DIR, 'static')]
    else:
        # Otherwise, for development mode
        settings.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        settings.TEMPLATES[0]['DIRS'] = [os.path.join(settings.BASE_DIR, 'myapp/templates')]
        settings.STATICFILES_DIRS = [os.path.join(settings.BASE_DIR, 'myapp/static')]

    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:2807', '--noreload'])

if __name__ == '__main__':
    # Run the Django server in a separate thread (main thread runs webview)
    run_django_server()

    # Once the server is running, create the webview window
    webview.create_window('My Django App', 'http://127.0.0.1:2807')
    webview.start()  # Start the webview window