from pypdf import PdfReader
import requests
import io

def load_resume(file_path):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        response = requests.get(file_path)
        response.raise_for_status()
        reader = PdfReader(io.BytesIO(response.content))
    else:
        reader = PdfReader(file_path)
    
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks