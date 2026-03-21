"""
Deploy script for AshAI Chatbot to Hugging Face Spaces
"""
from huggingface_hub import HfApi, login
import os

# Get token from environment or user input
token = os.getenv("HF_TOKEN") or input("Enter your Hugging Face token: ")

# Login
print("Logging in...")
login(token=token)

# Initialize API
api = HfApi()

repo_id = "Aashutosh724/GradioApp"

# Create Space
print("Creating Space...")
try:
    api.create_repo(
        repo_id=repo_id,
        repo_type="space",
        space_sdk="gradio",
    )
    print("Space created!")
except Exception as e:
    print(f"Space creation: {e}")

# Upload files
print("Uploading files...")
api.upload_folder(
    folder_path=".",
    repo_id=repo_id,
    repo_type="space",
    ignore_patterns=["venv/**", "__pycache__/**", ".git/**", "*.pyc", ".env", "chroma_db/**"],
)

print("✅ Deployment complete!")
print("Go to: https://huggingface.co/spaces/Aashutosh724/GradioApp")
