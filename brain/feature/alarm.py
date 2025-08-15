import datetime
import time
import threading
import os
import platform

def play_alarm_sound():
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 1000)  # Beep at 1000 Hz for 1 sec
    else:
        os.system('say "Alarm!"')  # macOS alternative (or use `playsound`)

def alarm_thread(alarm_time_str, speak=None, message="Wake up!"):
    alarm_time = datetime.datetime.strptime(alarm_time_str, "%H:%M").time()
    if speak:
        speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}")

    while True:
        now = datetime.datetime.now().time()
        if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
            if speak:
                speak(message)
            play_alarm_sound()
            break
        time.sleep(10)  # Check every 10 seconds

def set_alarm(alarm_time_str, speak=None, message="Time's up!"):
    """
    alarm_time_str: in "HH:MM" 24-hour format
    """
    thread = threading.Thread(target=alarm_thread, args=(alarm_time_str, speak, message))
    thread.start()
    return f"Alarm set for {alarm_time_str}"
