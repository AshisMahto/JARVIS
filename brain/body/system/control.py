import os
import platform
import subprocess

def shutdown(speak=None):
    try:
        os.system("shutdown /s /t 1")
        if speak:
            speak("Shutting down the computer.")
    except Exception as e:
        if speak:
            speak("Failed to shut down.")
        return str(e)

def restart(speak=None):
    try:
        os.system("shutdown /r /t 1")
        if speak:
            speak("Restarting the computer.")
    except Exception as e:
        if speak:
            speak("Failed to restart.")
        return str(e)

def logout(speak=None):
    try:
        os.system("shutdown -l")
        if speak:
            speak("Logging out.")
    except Exception as e:
        if speak:
            speak("Failed to log out.")
        return str(e)

def lock(speak=None):
    try:
        if platform.system() == "Windows":
            ctypes = __import__('ctypes')
            ctypes.windll.user32.LockWorkStation()
            if speak:
                speak("System locked.")
        else:
            if speak:
                speak("Lock command not supported on this OS.")
    except Exception as e:
        if speak:
            speak("Failed to lock the system.")
        return str(e)

def sleep(speak=None):
    try:
        if platform.system() == "Windows":
            subprocess.call("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            if speak:
                speak("Putting system to sleep.")
        else:
            if speak:
                speak("Sleep command not supported on this OS.")
    except Exception as e:
        if speak:
            speak("Failed to put the system to sleep.")
        return str(e)
