import resend
from dotenv import load_dotenv
import os

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

def send_email_to_owner(user_name, user_email, query):
    try:
        response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": os.getenv("OWNER_EMAIL"),
            "subject": f"New Lead from AshAI: {user_name}",
            "html": f"""
                <h3>New Lead!</h3>
                <p><strong>Name:</strong> {user_name}</p>
                <p><strong>Email:</strong> {user_email}</p>
                <p><strong>Query:</strong> {query}</p>
            """
        })
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
