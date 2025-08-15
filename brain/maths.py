import requests

# Replace with your WolframAlpha App ID
APP_ID = "your_wolframalpha_app_id"

def solve_math(query, speak=None):
    base_url = "http://api.wolframalpha.com/v1/result"
    params = {
        "i": query,
        "appid": APP_ID
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            answer = response.text
            if speak:
                speak(f"The answer is: {answer}")
            return answer
        else:
            if speak:
                speak("Sorry, I couldn't solve that.")
            return "WolframAlpha could not process the query."
    except Exception as e:
        if speak:
            speak("An error occurred while solving the math problem.")
        return f"Error: {e}"
