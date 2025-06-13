MODELS_HISTORY = {
    "deepseek": {"questions": [], "answers": []},
    "gryphe": {"questions": [], "answers": []},
    "mistralai": {"questions": [], "answers": []},
    "anthropic": {"questions": [], "answers": []},
    "llama3": {"questions": [], "answers": []},
    "flux": {"questions": [], "answers": []},
}


def add_to_history(model_name, question, answer):
    MODELS_HISTORY[model_name]["questions"].append(question)
    MODELS_HISTORY[model_name]["answers"].append(answer)
