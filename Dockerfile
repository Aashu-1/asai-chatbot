FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir "gradio[oauth]==4.44.0" "uvicorn>=0.14.0" "websockets>=10.4" spaces

COPY . .

CMD ["python", "app.py"]
