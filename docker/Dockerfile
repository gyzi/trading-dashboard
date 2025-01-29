# Use Python 3.12 (latest)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy only required files
COPY requirements.txt /app/
COPY dashboard.py /app/
COPY README.md /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run dashboard
ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]