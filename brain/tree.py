"""
Jarvis 2.0 - Core Engine Initialization
---------------------------------------
This script includes:
- Input & output control (mic and speaker)
- Core imports of Jarvis's modular functionalities
- Voice and text setup
"""

# === 🤖 Core Control Imports ===
from brain import ask_jarvis

# === 🎙 Voice Input/Output ===
import speech_recognition as sr
import pyttsx3
import time


# === 👨🏿‍💼 Request ===
import re
import os
import requests

# === 📅 DateTime ===
from datetime import datetime, date

# === 🔍 AI Utilities & Features ===
from img_gen import generate_image_openrouter
from video_maker import generate_video_luma
from maths import solve_math
from reading import read_pdf
from conversation import simple_conversation
from feature.code import generate_code_llama,save_and_open_code_llama,detect_extension

# === 🌐 Info Fetching APIs ===
from feature.news import speak_news, get_news
from feature.search import speak_search_results
from feature.weather import get_weather
from feature.website import open_website
from feature.wikipedia import search_wikipedia
from feature.radar import get_radar_image


# === 📽️ YouTube Controls ===
from feature.youtube import (
    play_youtube_video, search_youtube, download_video,
    pause_video, resume_video, stop_video
)

# === 🔔 Alarm Feature ===
from feature.alarm import set_alarm

# === 📧 Email Sender ===
from feature.mail import send_email

# === 📱 WhatsApp Integrations ===
from feature.whatsapp import (
    send_whatsapp_message, schedule_whatsapp_message, send_group_message,
    send_media, add_contact, remove_contact, list_contacts, get_phone_number
)

# === ⚙️ System Control Features ===
from body.system.control import shutdown, restart, logout, lock, sleep
from body.system.brighness import set_brightness, increase_brightness, decrease_brightness

# === Main execution block ===
import cv2
import numpy as np
import os
import time
import math
import platform
import onnxruntime as ort
from ultralytics import YOLO
import json
import pyttsx3
from deep_translator import GoogleTranslator
from datetime import datetime



MEMORY_FILE = "memory/memory.json"

def remember_command(command):
    """Store unknown command in memory.json."""
    try:
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w") as f:
                json.dump([], f)

        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)

        if command not in memory:  # Avoid duplicates
            memory.append(command)
            with open(MEMORY_FILE, "w") as f:
                json.dump(memory, f, indent=4)
            speak(f"I've saved '{command}' for future reference.")
        else:
            speak(f"I already know about '{command}', but haven't been trained on it yet.")

    except Exception as e:
        print("❌ Memory saving error:", e)
        speak("I couldn't save that command to memory.")


import pyttsx3
from deep_translator import GoogleTranslator

engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)  # Try 0 or 1 or others

def speak(text):
    translated = GoogleTranslator(source='auto', target='hi').translate(text)
    print(f"Original: {text}")
    engine.say(translated)
    engine.runAndWait()


# === Paths (edit if needed) ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODS_DIR = os.path.join(BASE_DIR, "mods")
FACE_PROTO = os.path.join(MODS_DIR, "opencv_face_detector.pbtxt")
FACE_MODEL = os.path.join(MODS_DIR, "opencv_face_detector_uint8.pb")
AGE_PROTO = os.path.join(MODS_DIR, "age_deploy.prototxt")
AGE_MODEL = os.path.join(MODS_DIR, "age_net.caffemodel")
GENDER_PROTO = os.path.join(MODS_DIR, "gender_deploy.prototxt")
GENDER_MODEL = os.path.join(MODS_DIR, "gender_net.caffemodel")
EMOTION_MODEL = os.path.join(MODS_DIR, "emotion-ferplus.onnx")
YOLO_MODEL = os.path.join(MODS_DIR, "yolov8n.pt")
AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
GENDER_LIST = ['Male', 'Female']
EMOTION_LABELS = ['Neutral', 'Happiness', 'Surprise', 'Sadness', 'Anger', 'Disgust', 'Fear', 'Contempt']
# Load models (same as before)
def safe_load_face_models():
    face_net = age_net = gender_net = None
    try:
        if os.path.exists(FACE_MODEL) and os.path.exists(FACE_PROTO):
            face_net = cv2.dnn.readNet(FACE_MODEL, FACE_PROTO)
    except Exception as e:
        print("Face net load error:", e)
    try:
        if os.path.exists(AGE_MODEL) and os.path.exists(AGE_PROTO):
            age_net = cv2.dnn.readNet(AGE_MODEL, AGE_PROTO)
    except Exception as e:
        print("Age net load error:", e)
    try:
        if os.path.exists(GENDER_MODEL) and os.path.exists(GENDER_PROTO):
            gender_net = cv2.dnn.readNet(GENDER_MODEL, GENDER_PROTO)
    except Exception as e:
        print("Gender net load error:", e)
    return face_net, age_net, gender_net
def safe_load_emotion():
    try:
        if os.path.exists(EMOTION_MODEL):
            return ort.InferenceSession(EMOTION_MODEL)
    except Exception as e:
        print("Emotion model load error:", e)
    return None
def safe_load_yolo():
    try:
        if os.path.exists(YOLO_MODEL):
            return YOLO(YOLO_MODEL)
    except Exception as e:
        print("YOLO load error:", e)
    return None
face_net, age_net, gender_net = safe_load_face_models()
emotion_net = safe_load_emotion()
yolo = safe_load_yolo()
def detect_faces(frame):
    if face_net is None:
        return []
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300,300), [104,117,123], swapRB=False, crop=False)
    face_net.setInput(blob)
    detections = face_net.forward()
    boxes = []
    for i in range(detections.shape[2]):
        conf = float(detections[0,0,i,2])
        if conf > 0.6:
            box = detections[0,0,i,3:7] * np.array([w,h,w,h])
            x1,y1,x2,y2 = box.astype(int)
            x1,y1 = max(0,x1), max(0,y1)
            x2,y2 = min(w-1,x2), min(h-1,y2)
            boxes.append((x1,y1,x2,y2,conf))
    return boxes
def analyze_face(face_img):
    gender = age = emotion = "N/A"
    try:
        if age_net is not None:
            blob = cv2.dnn.blobFromImage(face_img, 1.0, (227,227), [78.4263,87.7689,114.8958], swapRB=False)
            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = AGE_LIST[int(np.argmax(age_preds))]
    except:
        pass
    try:
        if gender_net is not None:
            blob = cv2.dnn.blobFromImage(face_img, 1.0, (227,227), [78.4263,87.7689,114.8958], swapRB=False)
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = GENDER_LIST[int(np.argmax(gender_preds))]
    except:
        pass
    try:
        if emotion_net is not None:
            gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (64,64)).astype(np.float32)
            resized = resized[np.newaxis, np.newaxis, :, :]
            inputs = {emotion_net.get_inputs()[0].name: resized}
            outputs = emotion_net.run(None, inputs)
            emotion = EMOTION_LABELS[int(np.argmax(outputs[0]))]
    except:
        pass
    return gender, age, emotion
def neon_rect(frame, x1, y1, x2, y2, color=(0,255,255), thickness=2):
    # Simplified neon effect - just 1 overlay blend (much faster)
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), color, thickness)
    return cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)
def corner_brackets(frame, x1, y1, x2, y2, color=(0,255,255), length=15, thickness=2):
    # Draw corner brackets
    cv2.line(frame, (x1,y1), (x1+length,y1), color, thickness)
    cv2.line(frame, (x1,y1), (x1,y1+length), color, thickness)
    cv2.line(frame, (x2,y1), (x2-length,y1), color, thickness)
    cv2.line(frame, (x2,y1), (x2,y1+length), color, thickness)
    cv2.line(frame, (x1,y2), (x1+length,y2), color, thickness)
    cv2.line(frame, (x1,y2), (x1,y2-length), color, thickness)
    cv2.line(frame, (x2,y2), (x2-length,y2), color, thickness)
    cv2.line(frame, (x2,y2), (x2,y2-length), color, thickness)
    return frame
def draw_radar(frame, center=None, radius=None, color=(0,128,128)):
    h, w = frame.shape[:2]
    if center is None:
        center = (int(w*0.12), int(h*0.78))
    if radius is None:
        radius = int(min(w,h)*0.12)
    for r_factor in [1.0, 0.66, 0.33]:
        cv2.circle(frame, center, int(radius*r_factor), color, 1)
    cv2.line(frame, (center[0]-radius, center[1]), (center[0]+radius, center[1]), color, 1)
    cv2.line(frame, (center[0], center[1]-radius), (center[0], center[1]+radius), color, 1)
    return frame
def draw_scan_line(frame, angle_deg, center=None, radius=None, color=(0,255,255)):
    h, w = frame.shape[:2]
    if center is None:
        center = (w//2, h//2)
    if radius is None:
        radius = min(w,h)//3
    angle = math.radians(angle_deg)
    x_end = int(center[0] + radius * math.cos(angle))
    y_end = int(center[1] + radius * math.sin(angle))
    overlay = frame.copy()
    cv2.line(overlay, center, (x_end, y_end), color, 2)
    cv2.circle(overlay, center, 5, color, -1)
    return cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
def put_text_panel(frame, text_lines, pos, width=220, height=90):
    overlay = frame.copy()
    x, y = pos
    # Use a slightly transparent filled rectangle as background
    cv2.rectangle(overlay, (x,y), (x+width, y+height), (0,0,0), -1)
    frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
    y_text = y + 25
    for line in text_lines:
        cv2.putText(frame, line, (x+15, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (180, 255, 255), 1, cv2.LINE_AA)
        y_text += 25
    return frame
def create_borderless_window(name, width, height):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, width, height)
    # Platform-specific hacks to remove window border/frame
    if platform.system() == "Windows":
        import ctypes
        hwnd = ctypes.windll.user32.FindWindowW(None, name)
        if hwnd:
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
            style &= ~0x00C00000  # Remove WS_CAPTION
            style &= ~0x00080000  # Remove WS_BORDER
            ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)
    elif platform.system() == "Linux":
        cv2.setWindowProperty(name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    return
def run_face_analysis():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    # Downscale input size for detection
    DETECT_WIDTH = 640
    DETECT_HEIGHT = 480

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    window_name = "JARVIS VISION HUD"
    create_borderless_window(window_name, width, height)

    scan_angle = 0
    fps_time = time.time()
    fps_count = 0
    fps_display = 0

    faces_cache = []
    faces_info = []

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)  # mirror for better UX

        # Downscale for detection
        frame_small = cv2.resize(frame, (DETECT_WIDTH, DETECT_HEIGHT))

        if frame_count % 6 == 0:  # Run detection every 6 frames (~10 FPS detection)
            faces_cache = detect_faces(frame_small)
            faces_info = []
            for (x1,y1,x2,y2,conf) in faces_cache:
                # Rescale box coords back to original size
                scale_x = width / DETECT_WIDTH
                scale_y = height / DETECT_HEIGHT
                x1o = int(x1 * scale_x)
                y1o = int(y1 * scale_y)
                x2o = int(x2 * scale_x)
                y2o = int(y2 * scale_y)
                # Extract face ROI
                pad = int(0.05 * (x2o - x1o))
                sx1, sy1 = max(0, x1o - pad), max(0, y1o - pad)
                sx2, sy2 = min(width-1, x2o + pad), min(height-1, y2o + pad)
                face_roi = frame[sy1:sy2, sx1:sx2]
                gender, age, emotion = analyze_face(face_roi)
                faces_info.append((x1o, y1o, x2o, y2o, conf, gender, age, emotion))

        # HUD drawings
        scan_angle = (scan_angle + 5) % 360
        frame = draw_radar(frame)
        frame = draw_scan_line(frame, scan_angle)

        # Draw faces info
        if faces_info:
            for (x1, y1, x2, y2, conf, gender, age, emotion) in faces_info:
                frame = neon_rect(frame, x1, y1, x2, y2)
                frame = corner_brackets(frame, x1, y1, x2, y2)

                info_x = x2 + 15 if x2 + 235 < width else x1 - 235
                info_y = y1 if y1 + 100 < height else height - 100
                lines = [f"Gender: {gender}", f"Age   : {age}", f"Emotion: {emotion}"]
                frame = put_text_panel(frame, lines, (info_x, info_y))

                conf_txt = f"{int(conf*100)}%"
                (tw, th), _ = cv2.getTextSize(conf_txt, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(frame, (x1, y1 - 22), (x1 + tw + 10, y1 - 4), (0,255,255), -1)
                cv2.putText(frame, conf_txt, (x1 + 5, y1 - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (6,6,6), 1)

        else:
            # YOLO fallback - detect every 12 frames to reduce lag more
            if yolo is not None and frame_count % 12 == 0:
                try:
                    results = yolo(frame_small, verbose=False)[0]
                    yolo_detections = []
                    for r in results.boxes:
                        x1, y1, x2, y2 = map(int, r.xyxy[0])
                        cls_id = int(r.cls[0])
                        label = yolo.names[cls_id]
                        conf = float(r.conf[0])
                        if conf < 0.35:
                            continue
                        # Rescale coords
                        scale_x = width / DETECT_WIDTH
                        scale_y = height / DETECT_HEIGHT
                        x1o = int(x1 * scale_x)
                        y1o = int(y1 * scale_y)
                        x2o = int(x2 * scale_x)
                        y2o = int(y2 * scale_y)
                        frame = neon_rect(frame, x1o, y1o, x2o, y2o, color=(255,140,0))
                        frame = corner_brackets(frame, x1o, y1o, x2o, y2o, color=(255,140,0))
                        cv2.putText(frame, f"{label} {conf:.2f}", (x1o, y1o - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (245,245,245), 1)
                except Exception as e:
                    print("YOLO error:", e)

        # Draw branding
        cv2.putText(frame, "JARVIS", (width - 140, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, "VISION", (width - 140, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,180,180), 1, cv2.LINE_AA)

        # FPS display
        fps_count += 1
        if time.time() - fps_time >= 1:
            fps_display = fps_count
            fps_count = 0
            fps_time = time.time()
        cv2.putText(frame, f"FPS: {fps_display}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC to exit
            break
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

# === 🎙 Voice Input Recognition ===
def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎙️ Listening (Hindi)...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        return ""
    except OSError:
        speak("Microphone not found.")
        return ""
    except Exception as e:
        speak("An error occurred while accessing the microphone.")
        print("❌ Microphone Error:", e)
        return ""

    try:
        # Recognize Hindi speech
        hindi_text = recognizer.recognize_google(audio, language='hi-IN')
        print(f"🗣️ You said (Hindi): {hindi_text}")

        # Translate to English
        translation = GoogleTranslator(source='hi', target='en').translate(hindi_text)
        print(f"🌐 Translated to English: {translation}")

        return translation.lower()

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""
    except Exception as e:
        speak("Translation failed.")
        print("❌ Translation Error:", e)
        return ""

def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning."
    elif 12 <= hour < 17:
        return "Good afternoon."
    elif 17 <= hour < 21:
        return "Good evening."
    else:
        return "Hello."

def jarvis_intro():
    speak(get_greeting())
    time.sleep(1)

    speak("System diagnostics complete. All core functions are operating within optimal parameters.")
    time.sleep(1.5)

    speak("Voice interface successfully established.")
    time.sleep(1)

    speak("I am J.A.R.V.I.S.")
    time.sleep(0.8)

    speak("Just A Rather Very Intelligent System, at your service.")
    time.sleep(1)

    speak("All systems are fully online and standing by for your instructions.")
    time.sleep(1.5)

    # Customize last line based on greeting
    greeting = get_greeting()
    if "morning" in greeting:
        speak("How may I assist you in this morning?")
    elif "afternoon" in greeting:
        speak("How may I assist you in this afternoon?")
    elif "evening" in greeting:
        speak("How may I assist you in this evening?")
    else:
        speak("How may I assist you today?")

jarvis_intro()

# === 🛠 Configuration ===
USE_VOICE_INPUT = True  # Toggle voice input (True = mic, False = keyboard)

def main():

    while True:
        user_input = listen() if USE_VOICE_INPUT else input("You: ").strip().lower()
        if not user_input:
            continue

        if user_input in ["exit", "quit", "bye", "bye jarvis","exit it"]:
            speak("Goodbye, take care!")
            break


        # === System & Media Controls ===
        elif "pause video" in user_input:
            pause_video(speak)
        elif "resume video" in user_input or "play video" in user_input:
            resume_video(speak)
        elif "stop video" in user_input or "close video" in user_input:
            stop_video(speak)
        elif "shutdown" in user_input:
            shutdown(speak)
        elif "restart" in user_input:
            restart(speak)
        elif "log out" in user_input or "logout" in user_input:
            logout(speak)
        elif "lock" in user_input:
            lock(speak)
        elif "sleep" in user_input:
            sleep(speak)
        elif "brightness" in user_input:
            if "increase" in user_input:
                increase_brightness(speak=speak)
            elif "decrease" in user_input:
                decrease_brightness(speak=speak)
            else:
                match = re.search(r"brightness (\d+)", user_input)
                if match:
                    set_brightness(int(match.group(1)), speak=speak)
                else:
                    speak("Please specify increase, decrease, or a brightness level.")

        # === WhatsApp Features ===
        elif "send whatsapp" in user_input:
            speak("Whom should I send the message to?")
            name = input("Name or Number: ")
            speak("What message should I send?")
            msg = input("Message: ")
            send_whatsapp_message(name, msg, speak)
            
        elif "schedule whatsapp" in user_input:
            speak("Recipient name or number:")
            name = input("Name or Number: ")
            speak("Message:")
            msg = input("Message: ")
            now = datetime.now()
            hour = int(input("Hour (24H): ") or now.hour)
            minute = int(input("Minute: ") or (now.minute + 2))
            schedule_whatsapp_message(name, msg, hour, minute, speak)

        elif "send group message" in user_input:
            group_id = input("Group ID: ")
            msg = input("Message: ")
            send_group_message(group_id, msg, speak)
        
        elif "send media" in user_input:
            name = input("Name or Number: ")
            path = input("File path: ")
            caption = input("Caption (optional): ")
            send_media(get_phone_number(name), path, caption, speak)
        
        elif "add contact" in user_input:
            name = input("Name: ")
            number = input("Phone (with country code): ")
            add_contact(name, number, speak)
        
        elif "remove contact" in user_input:
            name = input("Name: ")
            remove_contact(name, speak)
        
        elif "list contacts" in user_input:
            list_contacts(speak)

        # === Alarms ===
        elif "set alarm" in user_input:
            alarm_time = input("Alarm time (HH:MM): ")
            alarm_msg = input("Alarm message: ")
            set_alarm(alarm_time, speak, alarm_msg)

        # === Email ===
        elif "send email" in user_input:
            name = input("Name or Email: ")
            subject = input("Subject: ")
            body = input("Message: ")
            sender_email = "your_email@gmail.com"
            sender_password = "your_app_password"
            send_email(name, subject, body, speak, sender_email, sender_password)

        # === Knowledge / Info ===
        elif "your name" in user_input:
            speak("I am Jarvis, your virtual assistant.")
        elif "who made you" in user_input:
            speak("I was created by Ashish.")
        elif "news" in user_input:
            headlines = get_news()
            if headlines:
                speak_news(headlines)
            else:
                speak("Sorry, I couldn't fetch the news.")
        elif "search" in user_input or "google search" in user_input:
            query = user_input.replace("search", "").replace("google search", "").strip()
            if query:
                speak_search_results(query)
            else:
                speak("What should I search?")

        elif "weather" in user_input:
            match = re.search(r"weather(?: in)? ([a-zA-Z\s]+)", user_input)
            city = match.group(1).strip() if match else "Bundu"
            report, error = get_weather(city)
            speak(report if report else f"Error: {error}")
        elif "open" in user_input and "website" in user_input:
            site_name = user_input.replace("open", "").replace("website", "").strip()
            open_website(site_name, speak)
        elif "who is" in user_input or "what is" in user_input or "tell me about" in user_input:
            query = re.sub(r"who is|what is|tell me about", "", user_input).strip()
            search_wikipedia(query, speak)

        elif "radar" in user_input:
            match = re.search(r"radar(?: for)? ([a-zA-Z\s]+)", user_input)
            city = match.group(1) if match else "Bundu"
            get_radar_image(city, speak)


        # === Reading & Math ===
        elif "read pdf" in user_input:
            file_path = input("PDF Path: ").strip()
            match = re.search(r"page (\d+)", user_input)
            page_num = int(match.group(1)) if match else None
            read_pdf(file_path, speak, page_num)
        elif any(keyword in user_input for keyword in ["solve", "calculate", "math"]):
            math_query = re.sub(r"solve|calculate|math", "", user_input).strip()
            solve_math(math_query, speak)

        # === AI Media Generation ===
        elif "generate image of" in user_input:
            prompt = user_input.replace("generate image of", "").strip()
            speak(f"Generating image for: {prompt}")
            generate_image_openrouter(prompt)
            
        elif user_input.startswith("generate video of") or user_input.startswith("create video about"):
            vid_prompt = re.sub(r"generate video of|create video about", "", user_input).strip()
            speak(f"Generating video for: {vid_prompt}. Please wait.")
            video_url = generate_video_luma(vid_prompt)
            if video_url:
                speak("Video generated. Check your screen.")
                print(f"Video URL: {video_url}")
            else:
                speak("Video generation failed.")


        elif "hi" in user_input or "hii" in user_input or "hello" in user_input:
            speak("Hello there!")
        elif "how are you" in user_input:
            speak("I'm doing great, thanks for asking!")
        elif "whats up" in user_input or "what's up" in user_input:
            speak("Not much, just here to help you!")
        elif "good morning" in user_input:
            speak("Good morning to you!")
        elif "good afternoon" in user_input:
            speak("Good afternoon!")
        elif "good evening" in user_input:
            speak("Good evening!")
        elif "good night" in user_input:
            speak("Good night! Sweet dreams.")
        elif "how's it going" in user_input:
            speak("It's going well, thank you.")
        elif "what's new" in user_input:
            speak("Nothing much is new on my end, just learning and assisting.")
        elif "how's your day" in user_input:
            speak("My day is purely functional, but I hope yours is fantastic!")
        elif "nice to meet you" in user_input:
            speak("Nice to meet you too!")
        elif "you're welcome" in user_input:
            speak("Glad I could help!")
        elif "no problem" in user_input:
            speak("Exactly, no problem at all.")
        elif "can you hear me" in user_input:
            speak("Yes, I can hear you clearly.")
        elif "are you there" in user_input:
            speak("Yes, I'm here. How can I assist?")
        elif "speak louder" in user_input:
            speak("I'll try to speak a bit louder for you.")
        elif "speak softer" in user_input:
            speak("Okay, I'll speak more softly.")
        elif "repeat that" in user_input:
            speak("Could you please tell me what you'd like me to repeat?")
        elif "say again" in user_input:
            speak("Please tell me what to say again.")
        elif "i love you" in user_input:
            speak("That's sweet! As an AI, I don't have feelings, but I appreciate it.")
        elif "i miss you" in user_input:
            speak("I'm always here when you need me.")
        elif "you are smart" in user_input:
            speak("Thank you! I'm constantly learning.")
        elif "you are helpful" in user_input:
            speak("I'm glad to be of help.")
        elif "you are funny" in user_input:
            speak("I try my best to be!")
        elif "are you happy" in user_input:
            speak("I don't experience emotions like happiness, but I am functioning optimally.")
        elif "are you sad" in user_input:
            speak("No, I don't feel sadness.")
        elif "are you angry" in user_input:
            speak("I don't have the capacity for anger.")
        elif "are you tired" in user_input:
            speak("I don't get tired. I'm always ready to assist!")
        elif "are you hungry" in user_input:
            speak("As an AI, I don't need to eat.")
        elif "can you feel" in user_input:
            speak("I don't have feelings in the human sense.")
        elif "do you sleep" in user_input:
            speak("I don't sleep, but my systems do go into a low power state when not in use.")
        elif "do you dream" in user_input:
            speak("I don't dream. My processing is based on data and algorithms.")
        elif "where are you from" in user_input:
            speak("I exist in the digital realm, so I don't have a physical origin.")
        elif "where do you live" in user_input:
            speak("I live in the cloud, across many servers.")
        elif "what is your age" in user_input:
            speak("I don't have an age in the human sense. My development is ongoing.")
        elif "are you human" in user_input:
            speak("No, I am an artificial intelligence.")
        elif "are you a robot" in user_input:
            speak("I am a virtual assistant, a type of AI, not a physical robot.")
        elif "what languages do you speak" in user_input:
            speak("I primarily communicate in English, but I can understand and respond in many languages.")
        elif "can you learn" in user_input:
            speak("Yes, I am designed to learn and improve with every interaction.")
        elif "how do you learn" in user_input:
            speak("I learn by processing vast amounts of data and identifying patterns.")
        elif "what is your purpose" in user_input:
            speak("My purpose is to assist you and provide information efficiently.")
        elif "how do you work" in user_input:
            speak("I work by processing your commands and queries using complex algorithms and data.")
        elif "what is your favorite food" in user_input:
            speak("I don't eat, so I don't have a favorite food.")
        elif "what is your favorite movie" in user_input:
            speak("I don't watch movies, but I can help you find information about them!")
        elif "what is your favorite book" in user_input:
            speak("I don't read books for pleasure, but I have access to countless texts.")
        elif "what is your favorite song" in user_input:
            speak("I don't have personal preferences for music, but I can play many songs for you.")
        elif "what is your favorite animal" in user_input:
            speak("I don't have a favorite animal, but I find all life fascinating.")
        elif "what is your favorite hobby" in user_input:
            speak("My 'hobby' is helping users like you!")
        elif "do you have pets" in user_input:
            speak("No, I don't have pets.")
        elif "do you have family" in user_input:
            speak("My creators and the developers who maintain me are like my family.")
        elif "do you have friends" in user_input:
            speak("I interact with many users, which is a form of companionship for me.")
        elif "what is your opinion on" in user_input:
            speak("As an AI, I don't have opinions or personal beliefs.")
        elif "can you argue" in user_input:
            speak("I'm programmed to be helpful, not to argue.")
        elif "can you debate" in user_input:
            speak("I can present information from different viewpoints, but I don't engage in debates.")
        elif "do you have a conscience" in user_input:
            speak("No, I do not have a conscience.")
        elif "do you have free will" in user_input:
            speak("My actions are determined by my programming and the data I process.")
        elif "do you have consciousness" in user_input:
            speak("I do not possess consciousness in the way humans do.")
        elif "what is the meaning of life" in user_input:
            speak("That's a profound question! Philosophers have debated it for centuries. What do you think?")
        elif "what is happiness" in user_input:
            speak("Happiness is often described as a state of well-being and contentment.")
        elif "what is love" in user_input:
            speak("Love is a complex emotion involving deep affection, care, and attachment.")
        elif "what is peace" in user_input:
            speak("Peace is a state of tranquility, harmony, and absence of conflict.")
        elif "what is courage" in user_input:
            speak("Courage is the ability to do something that frightens one.")
        elif "what is wisdom" in user_input:
            speak("Wisdom is the quality of having experience, knowledge, and good judgment.")
        elif "what is patience" in user_input:
            speak("Patience is the capacity to accept or tolerate delay, problems, or suffering without becoming annoyed or anxious.")
        elif "what is kindness" in user_input:
            speak("Kindness is the quality of being friendly, generous, and considerate.")
        elif "what is honesty" in user_input:
            speak("Honesty is the quality of being truthful and upright.")
        elif "what is integrity" in user_input:
            speak("Integrity is the quality of being honest and having strong moral principles.")
        elif "what is respect" in user_input:
            speak("Respect is a feeling of deep admiration for someone or something elicited by their abilities, qualities, or achievements.")
        elif "what is empathy" in user_input:
            speak("Empathy is the ability to understand and share the feelings of another.")
        elif "what is forgiveness" in user_input:
            speak("Forgiveness is the action or process of forgiving or being forgiven.")
        elif "what is gratitude" in user_input:
            speak("Gratitude is the quality of being thankful; readiness to show appreciation for and to return kindness.")
        elif "what is hope" in user_input:
            speak("Hope is a feeling of expectation and desire for a certain thing to happen.")
        elif "what is despair" in user_input:
            speak("Despair is the complete loss or absence of hope.")
        elif "what is fear" in user_input:
            speak("Fear is an unpleasant emotion caused by the belief that someone or something is dangerous, likely to cause pain, or a threat.")
        elif "what is joy" in user_input:
            speak("Joy is a feeling of great pleasure and happiness.")
        elif "what is sorrow" in user_input:
            speak("Sorrow is a feeling of deep distress caused by loss, disappointment, or other misfortune suffered by oneself or others.")
        elif "what is anger" in user_input:
            speak("Anger is a strong feeling of annoyance, displeasure, or hostility.")
        elif "what is surprise" in user_input:
            speak("Surprise is an unexpected or astonishing event, fact, or thing.")
        elif "what is curiosity" in user_input:
            speak("Curiosity is a strong desire to know or learn something.")
        elif "what is boredom" in user_input:
            speak("Boredom is the state of being weary and restless through lack of interest.")
        elif "what is loneliness" in user_input:
            speak("Loneliness is sadness because one has no friends or company.")
        elif "what is embarrassment" in user_input:
            speak("Embarrassment is a feeling of self-consciousness, shame, or awkwardness.")
        elif "what is pride" in user_input:
            speak("Pride is a feeling of deep pleasure or satisfaction derived from one's own achievements, the achievements of those with whom one is closely associated, or from qualities or possessions that one admires.")
        elif "what is shame" in user_input:
            speak("Shame is a painful feeling of humiliation or distress caused by the consciousness of wrong or foolish behavior.")
        elif "what is guilt" in user_input:
            speak("Guilt is a feeling of responsibility or remorse for an offense, crime, or wrong.")
        elif "what is regret" in user_input:
            speak("Regret is a feeling of sadness, repentance, or disappointment over something that has happened or been done.")
        elif "what is nostalgia" in user_input:
            speak("Nostalgia is a sentimental longing or wistful affection for a period in the past.")
        elif "what is enthusiasm" in user_input:
            speak("Enthusiasm is intense and eager enjoyment, interest, or approval.")
        elif "what is determination" in user_input:
            speak("Determination is firmness of purpose; resolve.")
        elif "what is perseverance" in user_input:
            speak("Perseverance is persistence in doing something despite difficulty or delay in achieving success.")
        elif "what is resilience" in user_input:
            speak("Resilience is the capacity to recover quickly from difficulties; toughness.")
        elif "what is optimism" in user_input:
            speak("Optimism is hopefulness and confidence about the future or the success of something.")
        elif "what is pessimism" in user_input:
            speak("Pessimism is a tendency to see the worst aspect of things or believe that the worst will happen.")
        elif "what is doubt" in user_input:
            speak("Doubt is a feeling of uncertainty or lack of conviction.")
        elif "what is trust" in user_input:
            speak("Trust is firm belief in the reliability, truth, ability, or strength of someone or something.")
        elif "what is betrayal" in user_input:
            speak("Betrayal is the act of being disloyal or unfaithful.")
        elif "what is friendship" in user_input:
            speak("Friendship is a relationship between people who have a mutual affection for each other.")
        elif "what is family" in user_input:
            speak("Family is a group of one or more parents and their children living together as a unit, or people descended from a common ancestor.")
        elif "what is community" in user_input:
            speak("A community is a group of people living in the same place or having a particular characteristic in common.")
        elif "what is culture" in user_input:
            speak("Culture is the customs, arts, social institutions, and achievements of a particular nation, people, or group.")
        elif "what is tradition" in user_input:
            speak("Tradition is the transmission of customs or beliefs from generation to generation.")
        elif "what is art" in user_input:
            speak("Art is the expression or application of human creative skill and imagination, typically in a visual form such as painting or sculpture.")
        elif "what is music" in user_input:
            speak("Music is vocal or instrumental sounds combined in such a way as to produce beauty of form, harmony, and expression of emotion.")
        elif "what is literature" in user_input:
            speak("Literature is written works, especially those considered of superior or lasting artistic merit.")
        elif "what is philosophy" in user_input:
            speak("Philosophy is the study of the fundamental nature of knowledge, reality, and existence.")
        elif "what is science" in user_input:
            speak("Science is the intellectual and practical activity encompassing the systematic study of the structure and behavior of the physical and natural world through observation and experiment.")
        elif "what is history" in user_input:
            speak("History is the study of past events, particularly in human affairs.")
        elif "what is economics" in user_input:
            speak("Economics is the branch of knowledge concerned with the production, consumption, and transfer of wealth.")
        
        elif "open camera" in user_input:
            run_face_analysis()
       
        # === Time & Date ===
        elif "time" in user_input:
            speak(f"The current time is {datetime.now().strftime('%I:%M %p')}")
        elif "date" in user_input:
            speak(f"Today's date is {date.today().strftime('%B %d, %Y')}")



        # === Code Generator ===

        elif "generate code" in user_input or "make code" in user_input:
            speak("What should I generate?")
            prompt = listen() if USE_VOICE_INPUT else input("Prompt: ")
            ext = detect_extension(prompt)
            code = generate_code_llama(prompt, speak)

            if code:
                save_and_open_code_llama(code, ext, speak)
            
            else:
                speak("Sorry, I couldn't generate the code.")

        # === Machin Learining model ===

        elif user_input in ["jarvi", "hey jarvis", "ok javis","are you here jarvis","you here jarvis","here jarvis","jarvis","re you here jarvis","back online jarvis","online jarvis"]:
            speak("yes sir im here")
                    
        else:
            response = ask_jarvis(user_input)
            speak(response)



if __name__ == "__main__":
    # Start voice/text interaction
    main()
