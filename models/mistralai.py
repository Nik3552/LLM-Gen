import requests
from config.settings import openrouter_api_key
from utils import history


def query_mistralai(prompt):
    if len(prompt) <= 0:
        return

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": f"{prompt}"}],
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        answer = (
            response.json()["choices"][0]["message"]["content"]
            .encode("ascii", "ignore")
            .decode()
        )
        history.add_to_history("mistralai", prompt, answer)
        return answer
    except Exception as e:
        return f"Error from Gryphe API: {e}"
