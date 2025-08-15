import requests
import base64

API_KEY = "YOUR_OPENROUTER_API_KEYS"
IMAGE_OUTPUT = "generated_image.png"

def generate_image_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4o",  # Example model; update if needed
        "messages": [
            {"role": "user", "content": f"Generate an image of: {prompt}"}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            content = response.json()['choices'][0]['message']['content']
            image_data = content.split(",")[-1]  # Base64 part only
            with open(IMAGE_OUTPUT, "wb") as f:
                f.write(base64.b64decode(image_data))
            print(f"[✓] Image saved as {IMAGE_OUTPUT}")
        except Exception as e:
            print("[!] Image parsing error:", e)
    else:
        print("[!] Image generation failed:", response.status_code, response.text)
