import requests
from core.conf import OLLAMA_API_URL, OLLAMA_API_TOKEN

def call_agent_LLM(prompt, agent):
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OLLAMA_API_TOKEN}",
    }

    payload = {
        "model": agent,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            headers=headers,
            timeout=1500 #25 min de raisonement max
        )
        
        response.raise_for_status()
        
        result = response.json()
        if "response" in result:
            full_response = result["response"]
        
        return full_response
        
    except Exception as error:
        return ""

