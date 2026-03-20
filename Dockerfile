FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir gradio==5.9.0 gradio_client==1.4.0 openai==1.55.0 uvicorn websockets fsspec

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
