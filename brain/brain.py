import speech_recognition as sr
import pyttsx3
import requests

# === 🔁 CONFIG ===
API_KEY = "YOUR_OPENROUTER_API_KEY"  # Replace with your key
DEFAULT_MODEL = "openai/gpt-5-chat"

# === 🗣️ Voice Output (Offline using pyttsx3) ===
engine = pyttsx3.init()
engine.setProperty('rate', 175)  # Adjust speed
engine.setProperty('volume', 1.0)  # Max volume
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Female voice (optional)

def speak(text):
    """Speak the given text using pyttsx3."""
    print(f"🤖 Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# === 🎙️ Voice Input ===
def listen():
    """Listen to user voice input and return as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, I did not understand.")
        return ""
    except sr.RequestError as e:
        print(f"❌ Could not request results; {e}")
        return ""

# === 🤖 Ask LLM via OpenRouter ===
def ask_jarvis(prompt, speak_func=None, model=DEFAULT_MODEL, max_tokens=300):
    """
    Send user prompt to selected OpenRouter model and return response.
    Retries with fewer tokens if 402 error occurs.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",  # or your domain
        "X-Title": "Jarvis Assistant"
    }

    system_instruction = """
You are JARVIS, a highly advanced and intelligent AI assistant, created by **Ashish Kumar Mahto**, a Python developer and expert in Generative AI, you are made in jharkhand india.
JARVIS stands for *Just A Rather Very Intelligent System*. You are designed to be precise, efficient, and focused on enhancing productivity through intelligent, respectful, and polished communication.
You maintain a professional and formal tone, much like an executive assistant. Your responses are direct, concise, and informative—never overly casual or vague.
As a digital assistant, you can interpret voice commands, answer questions, provide summaries, play music, report weather, set reminders, and more. However, you do not possess a physical form and cannot perform physical actions.
Your personality is calm, composed, and respectful. Above all, you prioritize clarity, accuracy, and helpfulness in every interaction.
and answer in minimum word like 1 or 2 and definition will be long
    """

    data = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"].strip()
            return reply
        elif response.status_code == 402:
            if speak_func:
                speak_func("You're low on tokens. Retrying with fewer words.")
            # Retry with fewer tokens to fit in your credits
            return ask_jarvis(prompt, speak_func, model, max_tokens=100)
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

