import webbrowser

# Dictionary of common websites
WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "chatgpt": "https://chat.openai.com",
    "gmail": "https://mail.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://twitter.com",
    "github": "https://github.com",
    "stackoverflow": "https://stackoverflow.com",
    "instagram": "https://www.instagram.com",
    "netflix": "https://www.netflix.com",
    "amazon": "https://www.amazon.in"
}

def open_website(site_name, speak=None):
    """
    Opens the given website if available in the list.
    If 'speak' is passed (function), it will speak the result.
    """
    site_name = site_name.lower().strip()

    # Match website name
    for key in WEBSITES:
        if key in site_name:
            url = WEBSITES[key]
            webbrowser.open(url)
            if speak:
                speak(f"Opening {key}")
            return True

    if speak:
        speak("Sorry, I couldn't find that website.")
    return False
