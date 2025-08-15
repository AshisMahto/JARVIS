from serpapi import GoogleSearch

def speak_search_results(query, speak=None):
    params = {
        "engine": "google",
        "q": query,
        "api_key": "YOUR_SERPAPI_API_KEY"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "answer_box" in results:
        answer = results["answer_box"].get("answer") or results["answer_box"].get("snippet")
        if answer:
            if speak:
                speak(answer)
            return answer

    elif "organic_results" in results:
        first_result = results["organic_results"][0]["snippet"]
        if speak:
            speak(first_result)
        return first_result

    else:
        if speak:
            speak("Sorry, I couldn't find anything relevant.")
        return "No result found."
