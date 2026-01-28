from ollama import chat
from core.conf import SYSTEM_PROMPT, MODEL_LLM
import os


def call_agent_LLM(prompt, agent = MODEL_LLM):
    """
    Apelle un LLM, avec les prompt et retourne le résultat
    """
    response = chat(
        model=agent,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]
