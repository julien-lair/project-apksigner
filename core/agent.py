from ollama import chat
from core.conf import SYSTEM_PROMPT, MODEL_LLM


def call_agent_LLM(prompt):
    """
    Apelle un LLM, avec les prompt et retourne le résultat
    """
    response = chat(
        model=MODEL_LLM,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]
