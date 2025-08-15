import requests
import time

OPENROUTER_API_KEY = "your_openrouter_api_key"
LUMA_API_KEY = "your_luma_api_key"

def enhance_prompt_with_openrouter(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "anthropic/claude-3.5-sonnet",  # or another OpenRouter model
        "messages": [{"role": "user", "content": f"Enhance this video generation prompt: {prompt}"}]
    }
    resp = requests.post(url, headers=headers, json=data)
    resp_json = resp.json()
    return resp_json["choices"][0]["message"]["content"]

def generate_video_luma(prompt: str) -> str:
    # Step 1: Enhance prompt
    refined_prompt = enhance_prompt_with_openrouter(prompt)
    
    # Step 2: Send to Luma API
    headers = {
        "Authorization": f"Bearer {LUMA_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": refined_prompt,
        "model": "dream_machine",
        "duration": "5s",
        "resolution": "720p"
    }
    submit_url = "https://api.lumalabs.ai/dream-machine/v1/generations"
    response = requests.post(submit_url, headers=headers, json=data)
    resp_json = response.json()
    if response.status_code != 200 or "id" not in resp_json:
        return None

    video_id = resp_json["id"]

    # Step 3: Poll until video is ready
    poll_url = f"{submit_url}/{video_id}"
    while True:
        poll = requests.get(poll_url, headers=headers).json()
        status = poll.get("status")
        if status == "completed":
            return poll.get("video_url")
        elif status == "failed":
            return None
        time.sleep(5)
