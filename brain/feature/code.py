# ✅ Add Code Generator Feature (LLaMA + Voice Integration) to Jarvis

import requests
import os
import webbrowser

# === 🧠 Code Generator with LLaMA ===
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"  # Replace with your OpenRouter API key
LLAMA_MODEL = "meta-llama/llama-3-8b-instruct"

# --- Auto-detect file extension
def detect_extension(prompt):
    prompt = prompt.lower()
    if "html" in prompt:
        return "html"
    elif "css" in prompt:
        return "css"
    elif "javascript" in prompt or "js" in prompt:
        return "js"
    elif "python" in prompt or "py" in prompt:
        return "py"
    elif "php" in prompt:
        return "php"
    elif "c++" in prompt or "cpp" in prompt:
        return "cpp"
    elif "java" in prompt:
        return "java"
    else:
        return "txt"

# --- Clean and extract code only
def extract_code_only(content):
    if "</html>" in content:
        return content.split("</html>")[0] + "</html>"
    elif "```" in content:
        return "\n".join(content.split("```")[1:-1]).strip()
    return content

# --- Generate code using OpenRouter (LLaMA)
def generate_code_llama(prompt, speak=None):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": LLAMA_MODEL,
        "messages": [
            {"role": "user", "content": f"Only output code. {prompt}"}
        ]
    }

    if speak:
        speak("Generating code using LLaMA...")

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    try:
        result = response.json()
        if "choices" in result:
            code = result["choices"][0]["message"]["content"]
            return extract_code_only(code)
        else:
            if speak:
                speak("LLaMA did not return any code.")
            print("❌ Unexpected response:", result)
    except Exception as e:
        if speak:
            speak("Something went wrong while contacting LLaMA.")
        print("❌ Error:", e)
        print("Raw response:", response.text)
    return None

# --- Save and open code
def save_and_open_code_llama(code, ext, speak=None):
    filename = f"generated_code.{ext}"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    if speak:
        speak(f"Code saved as {filename}. Opening in VS Code now.")
    os.system(f"code {filename}")
    if ext == "html":
        webbrowser.open(f"file://{os.path.abspath(filename)}")
        if speak:
            speak("Also opening it in your browser.")
