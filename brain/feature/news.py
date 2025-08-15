import requests
import pyttsx3

API_KEY = 'YOUR_NEWS_API'  # Replace with your NewsAPI key
NEWS_API_URL = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={API_KEY}'

def get_news():
    try:
        response = requests.get(NEWS_API_URL)
        data = response.json()

        if data['status'] != 'ok':
            print("Failed to get news:", data.get('message', 'Unknown error'))
            return []

        articles = data.get('articles', [])
        headlines = [article['title'] for article in articles if article['title']]
        return headlines

    except Exception as e:
        print("Error fetching news:", e)
        return []

def speak_news(headlines):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.say("Here are the latest news headlines:")
    for headline in headlines[:5]:  # Limit to top 5 headlines
        print(headline)
        engine.say(headline)
    engine.runAndWait()

