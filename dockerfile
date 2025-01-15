# Use an official Python runtime as a parent image
FROM python:3.10

# Install dependencies for PyInstaller and mysqlclient
RUN apt-get update && \
    apt-get install -y gcc python3-dev build-essential \
    libgirepository1.0-dev cmake

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Install PyInstaller
RUN pip install pyinstaller

# Command to create the executable
CMD ["pyinstaller", "--onefile", "--add-data", "myapp/templates:myapp/templates", "desktop_app.py"]