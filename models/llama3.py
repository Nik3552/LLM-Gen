from groq import Groq
from config.settings import llama3_api_key
from utils import history


def query_llama3(prompt: str) -> str:
    if len(prompt) <= 0:
        return

    try:
        client = Groq(api_key=llama3_api_key)
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        answer = response.choices[0].message.content
        if answer:
            history.add_to_history("llama3", prompt, answer)

        return answer
    except Exception as e:
        return f"Error from LLaMA 3 API: {e}"
