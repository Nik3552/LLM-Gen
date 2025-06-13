import requests
from config.settings import deepseek_api_key
from utils import history


def query_deepseek(prompt):
    if len(prompt) <= 0:
        return

    API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"
    headers = {
        "Authorization": f"Bearer {deepseek_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "deepseek/deepseek-v3-0324",
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        answer = (
            response.json()["choices"][0]["message"]["content"]
            .encode("ascii", "ignore")
            .decode()
        )
        history.add_to_history("deepseek", prompt, answer)
        return answer
    except Exception as e:
        return f"Error from DeepSeek API: {e}"
