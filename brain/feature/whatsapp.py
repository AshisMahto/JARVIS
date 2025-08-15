import pywhatkit
import time
import os
import json
from datetime import datetime

# JSON file to store contacts
CONTACTS_FILE = "contacts.json"

# Load or initialize contacts
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

# Get phone number by name or return the input if direct number
def get_phone_number(name_or_number):
    contacts = load_contacts()
    name_or_number = name_or_number.lower().strip()
    return contacts.get(name_or_number, name_or_number)

# 1. Send WhatsApp Message Instantly
def send_whatsapp_message(identifier, message, speak=None, wait_time=10):
    try:
        phone_number = get_phone_number(identifier)
        pywhatkit.sendwhatmsg_instantly(phone_no=phone_number, message=message, wait_time=wait_time, tab_close=True)
        if speak:
            speak(f"Sending WhatsApp message to {identifier}")
        return "Message sent!"
    except Exception as e:
        if speak:
            speak("Failed to send the message.")
        return f"Error: {e}"

# 2. Schedule WhatsApp Message
def schedule_whatsapp_message(identifier, message, hour, minute, speak=None):
    try:
        phone_number = get_phone_number(identifier)
        pywhatkit.sendwhatmsg(phone_number, message, hour, minute)
        if speak:
            speak(f"Message scheduled for {identifier} at {hour}:{minute}")
        return "Message scheduled."
    except Exception as e:
        if speak:
            speak("Failed to schedule the message.")
        return f"Error: {e}"

# 3. Send WhatsApp Group Message
def send_group_message(group_id, message, speak=None):
    try:
        pywhatkit.sendwhatmsg_to_group_instantly(group_id=group_id, message=message, tab_close=True)
        if speak:
            speak("Sending message to group.")
        return "Group message sent!"
    except Exception as e:
        if speak:
            speak("Failed to send group message.")
        return f"Error: {e}"

# 4. Send Media File
def send_media(phone, file_path, caption="", speak=None):
    try:
        pywhatkit.sendwhats_image(receiver=phone, img_path=file_path, caption=caption, wait_time=10, tab_close=True)
        if speak:
            speak(f"Sending media to {phone}")
        return "Media sent!"
    except Exception as e:
        if speak:
            speak("Failed to send media.")
        return f"Error: {e}"

# 5. Contact Manager
def add_contact(name, number, speak=None):
    contacts = load_contacts()
    contacts[name.lower()] = number
    save_contacts(contacts)
    if speak:
        speak(f"Contact {name} added.")
    return "Contact saved."

def remove_contact(name, speak=None):
    contacts = load_contacts()
    if name.lower() in contacts:
        del contacts[name.lower()]
        save_contacts(contacts)
        if speak:
            speak(f"Contact {name} removed.")
        return "Contact removed."
    else:
        if speak:
            speak("Contact not found.")
        return "Not found."

def list_contacts(speak=None):
    contacts = load_contacts()
    if speak:
        for name, number in contacts.items():
            speak(f"{name.title()}: {number}")
    return contacts
