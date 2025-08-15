def simple_conversation(user_input, speak=None):
    user_input = user_input.lower().strip()

    responses = {
        "hi": "Hello!",
        "hello": "Hi there!",
        "hey": "Hey!",
        "how are you": "I'm doing great, thanks for asking!",
        "what's up": "All good! Ready to assist you.",
        "who are you": "I am Jarvis, your virtual assistant.",
        "thank you": "You're welcome!",
        "thanks": "Glad to help!",
        "good morning": "Good morning! Have a great day!",
        "good night": "Good night! Sleep well.",
        "bye": "Goodbye! See you soon.",
        "your inventor":"my inventor is ashish"
    }

    # Check for exact match or partial
    for phrase in responses:
        if phrase in user_input:
            reply = responses[phrase]
            if speak:
                speak(reply)
            return reply

    return None  # Let main fallback to ask_jarvis()
