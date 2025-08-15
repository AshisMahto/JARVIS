import wikipedia

# Set language if needed
wikipedia.set_lang("en")

def search_wikipedia(query, speak=None, sentences=2):
    try:
        summary = wikipedia.summary(query, sentences=sentences)
        if speak:
            speak(summary)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        if speak:
            speak("Your query is too broad. Please be more specific.")
        return "Disambiguation Error. Be more specific."
    except wikipedia.exceptions.PageError:
        if speak:
            speak("Sorry, I couldn't find any information on that topic.")
        return "Page not found."
    except Exception as e:
        if speak:
            speak("An error occurred while fetching information.")
        return f"Error: {e}"
