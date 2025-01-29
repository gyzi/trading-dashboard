FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt dashboard.py ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]