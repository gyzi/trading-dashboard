# Use the official Python image from Docker Hub
FROM python:3.7

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 8501 available for the app
EXPOSE 8501

# Run Streamlit when the container launches
ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
