import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_email_to_owner(user_name, user_email, query):
    print("Request received for tool calling ")
    print("username",user_name)
    print("user's email",user_email)
    print("query asked",query)
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("OWNER_EMAIL")

    subject = f"New Lead from AshAI: {user_name}"

    body = f"""
    New query received!

    Name: {user_name}
    Email: {user_email}
    Query: {query}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Email error:", e)
        return False