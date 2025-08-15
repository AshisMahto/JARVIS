import screen_brightness_control as sbc

def set_brightness(level, speak=None):
    """
    Set brightness to a specific level (0 to 100).
    """
    try:
        sbc.set_brightness(level)
        if speak:
            speak(f"Brightness set to {level} percent.")
        return f"Brightness set to {level}%"
    except Exception as e:
        if speak:
            speak("Failed to set brightness.")
        return f"Error: {e}"

def increase_brightness(step=10, speak=None):
    """
    Increase brightness by a certain percentage.
    """
    try:
        current = sbc.get_brightness(display=0)[0]
        new_level = min(current + step, 100)
        sbc.set_brightness(new_level)
        if speak:
            speak(f"Increasing brightness to {new_level} percent.")
        return f"Brightness increased to {new_level}%"
    except Exception as e:
        if speak:
            speak("Failed to increase brightness.")
        return f"Error: {e}"

def decrease_brightness(step=10, speak=None):
    """
    Decrease brightness by a certain percentage.
    """
    try:
        current = sbc.get_brightness(display=0)[0]
        new_level = max(current - step, 0)
        sbc.set_brightness(new_level)
        if speak:
            speak(f"Decreasing brightness to {new_level} percent.")
        return f"Brightness decreased to {new_level}%"
    except Exception as e:
        if speak:
            speak("Failed to decrease brightness.")
        return f"Error: {e}"
