# Set the base image to Python 3.9
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the files
COPY main.py .
COPY config.py .
COPY cogs/ cogs/
COPY Dockerfile Raven.db* ./

# Install the required Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the Python script
CMD [ "python3", "main.py" ]
