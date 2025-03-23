import requests
from config import OPENAI_API_KEY, GEMINI_API_KEY

def analyze_with_openai(content, api_key=OPENAI_API_KEY):
 
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": "Analyze the following video frame descriptions:"},
            {"role": "user", "content": content}
        ],
        "max_tokens": 300
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        raise ValueError(f"Error making OpenAI API request: {e}")


def analyze_with_gemini(content, api_key=GEMINI_API_KEY):
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gemini-v1",
        "messages": [
            {"role": "user", "content": "Analyze the following video frame descriptions:"},
            {"role": "user", "content": content}
        ],
        "max_tokens": 300
    }

    try:
        response = requests.post("https://api.gemini.ai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        raise ValueError(f"Error making Gemini API request: {e}")
