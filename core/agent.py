import requests
from core.conf import SYSTEM_PROMPT, MODEL_LLM
import os
import json

token_VASTAI = "" # pour obtneir baerer token  sur vast.ai : echo $OPEN_BUTTON_TOKEN

OLLAMA_API_URL = ":54863/api/generate"
OLLAMA_API_TOKEN = token_VASTAI

LLM_local = False

def call_agent_LLM(prompt, agent):

    headers = {
        "Content-Type": "application/json",
         "Authorization": f"Bearer {OLLAMA_API_TOKEN}",
    }

    payload = {
        "model": agent,
        "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}",
        "stream": False
    }

    response = requests.post(
        OLLAMA_API_URL,
        json=payload,
        headers=headers,
        timeout=600
    )
    response.raise_for_status()

    full_response = ""

    for line in response.text.splitlines():
        if not line.strip():
            continue
        chunk = json.loads(line)
        if "response" in chunk:
            full_response += chunk["response"]
    #print(full_response)
    return full_response


# def call_agent_LLM(prompt, agent=MODEL_LLM):
#     """
#      Apelle un LLM, avec les prompt et retourne le résultat
#     """

#     if LLM_local:
#         from ollama import chat
#         response = chat(
#         model=agent,
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": prompt}
#         ]
#         )
#         return response["message"]["content"]
#     else:
#         #on utilise llm dans cloud (location GPU -> vast.ai prix OK)
#         headers = {
#             "Authorization": f"Bearer {OLLAMA_API_TOKEN}",
#             "Content-Type": "application/json"
#         }

#         payload = {
#             "model": agent,
#             "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}"
#         }

#         response = requests.post(OLLAMA_API_URL, json=payload, headers=headers)
#         response.raise_for_status()  

#         data = response.json()
#         return data #data.get("response") or data.get("text")  
