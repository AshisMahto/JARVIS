import pywhatkit
from pytube import YouTube
from youtubesearchpython import VideosSearch
import os
import pyautogui
import time

def play_youtube_video(query, speak=None):
    try:
        if speak:
            speak(f"Playing {query} on YouTube.")
        pywhatkit.playonyt(query)
        time.sleep(5)  # Wait for browser to load
        pyautogui.press("space")  # Start playing
        return f"Playing {query} on YouTube."
    except Exception as e:
        if speak:
            speak("Sorry, I couldn't play that video.")
        return f"Error: {e}"

def search_youtube(query, speak=None, limit=5):
    try:
        videos = VideosSearch(query, limit=limit).result()["result"]
        result_list = []
        if speak:
            speak(f"Top {limit} YouTube results for {query}:")
        for i, video in enumerate(videos):
            title = video["title"]
            link = video["link"]
            if speak:
                speak(f"{i+1}: {title}")
            result_list.append(f"{i+1}. {title}\n{link}")
        return "\n\n".join(result_list)
    except Exception as e:
        if speak:
            speak("Sorry, YouTube search failed.")
        return f"Error: {e}"

def download_video(url, speak=None, audio_only=False):
    try:
        yt = YouTube(url)
        title = yt.title

        if audio_only:
            stream = yt.streams.filter(only_audio=True).first()
            out_file = stream.download()
            base, ext = os.path.splitext(out_file)
            new_file = base + ".mp3"
            os.rename(out_file, new_file)
            if speak:
                speak(f"Audio downloaded: {title}")
            return new_file
        else:
            stream = yt.streams.get_highest_resolution()
            file_path = stream.download()
            if speak:
                speak(f"Video downloaded: {title}")
            return file_path
    except Exception as e:
        if speak:
            speak("Failed to download the video.")
        return f"Error: {e}"

# 🔁 Media Controls

def pause_video(speak=None):
    pyautogui.press("space")
    if speak:
        speak("Video paused.")

def resume_video(speak=None):
    pyautogui.press("space")
    if speak:
        speak("Video resumed.")

def stop_video(speak=None):
    pyautogui.hotkey("ctrl", "w")
    if speak:
        speak("Video stopped and tab closed.")
