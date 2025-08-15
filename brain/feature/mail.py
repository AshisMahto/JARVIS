import smtplib
import ssl
import json
from email.message import EmailMessage
import os

# Load saved email contacts
def get_email_address(name):
    try:
        with open("contacts_email.json", "r") as file:
            contacts = json.load(file)
        return contacts.get(name.lower())
    except Exception as e:
        return None

# Send email
def send_email(name_or_email, subject, body, speak, sender_email, sender_password):
    # Try resolving name to email
    receiver_email = get_email_address(name_or_email) or name_or_email

    if not receiver_email or "@" not in receiver_email:
        speak("I couldn't find a valid email address.")
        return

    try:
        speak("Sending your email now...")
        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        speak(f"Email sent successfully to {name_or_email}.")

    except Exception as e:
        speak(f"Failed to send the email. Reason: {str(e)}")
