from core.agent import call_agent_LLM
from tqdm import tqdm
def structure_analyse(staticData, process=True):
    Category_methods = [
                "cryptography",
                "binary",
                "io",
                "network",
                "utils",
                "memory",
                "parsing",
                "system",
                "unknown"
            ]

    totalMethod = get_total_method(staticData)
    with tqdm(total=totalMethod, desc="Analyse des méthodes", unit="Méthode") as pbar:
        for data in staticData:
            context = data["context"]
            for method in data["methods"]:
                
                prompt = f"""
                You are a classifier.

                TASK:
                Classify the following method into EXACTLY ONE category.

                CATEGORIES:
                {Category_methods}

                RULES:
                - Answer with ONE WORD ONLY
                - The word MUST be in CATEGORIES
                - NO explanation
                - NO sentence
                - If unsure, answer: unknown
                
                CONTEXT:
                {context}

                METHOD:
                {method}

                Just one word please for the category.
                """
                if process:
                    res = call_agent_LLM(prompt,"qwen3:32b")
                    method["category"] = res.replace("\n","")
                """
                rapide : deepseek-coder:6.7b (mais sort des long text parfois)
                qwen3:32b : assez rapide environ 6 secondes par méthodes
                """
                pbar.update(1)
                
    return staticData

def get_total_method(data):
    res = 0
    for elem in data:
        res += len(elem["methods"])
    return res