# frontend/Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y build-essential libgomp1

RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
