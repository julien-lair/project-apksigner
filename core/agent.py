import requests
from core.conf import SYSTEM_PROMPT, MODEL_LLM
import os

ip_VASTAI = "1.1.1.1"
token_VASTAI = "azerty" # pour obtneir baerer token  sur vast.ai : echo $OPEN_BUTTON_TOKEN

OLLAMA_API_URL = f"http://{ip_VASTAI}:11434/api/generate"
OLLAMA_API_TOKEN = token_VASTAI

LLM_local = False
def call_agent_LLM(prompt, agent=MODEL_LLM):
    """
     Apelle un LLM, avec les prompt et retourne le résultat
    """

    if LLM_local:
        from ollama import chat
        response = chat(
        model=agent,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        )
        return response["message"]["content"]
    else:
        #on utilise llm dans cloud (location GPU -> vast.ai prix OK)
        headers = {
            "Authorization": f"Bearer {OLLAMA_API_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": agent,
            "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}"
        }

        response = requests.post(OLLAMA_API_URL, json=payload, headers=headers)
        response.raise_for_status()  

        data = response.json()
        return data #data.get("response") or data.get("text")  
