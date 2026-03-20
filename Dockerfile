FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir gradio==5.9.0 "uvicorn>=0.14.0" "websockets>=10.4"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
