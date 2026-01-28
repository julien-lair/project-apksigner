from core.agent import call_agent_LLM
from tools.save import save_in_file
from tqdm import tqdm
import time
def structure_analyse(staticData):
    print("je fais une analyse de la structure")
    
    allowed_categories = [
                "cryptography",
                "binary",
                "io",
                "network",
                "utils",
                "memory",
                "math",
                "parsing",
                "system",
                "unknown"
            ]

    i = 1
    totalMethod = get_total_method(staticData)
    with tqdm(total=totalMethod, desc="Analyse des méthodes", unit="method") as pbar:
        for data in staticData:
            context = get_context_of_class(data["signature"]["name"])
            for method in data["methods"]:
                
                prompt = f"""
                You are a classifier.

                TASK:
                Classify the following method into EXACTLY ONE category.

                CATEGORIES:
                {allowed_categories}

                RULES:
                - Answer with ONE WORD ONLY
                - The word MUST be in CATEGORIES
                - NO explanation
                - NO sentence
                - If unsure, answer: unknown


                METHOD:
                {method}
                """
                res = ""#call_agent_LLM(prompt,"deepseek-coder:6.7b")
                pbar.update(1)
                method["category"] = res.replace("\n","")
    return staticData

def get_context_of_class(className):
    path = "macro/"+ className+".md"
    try:
        with open(path, "r") as contextFile:
            return contextFile.read()
    except FileNotFoundError:
        return "No context for this class"

def get_total_method(data):
    res = 0
    for elem in data:
        res += len(elem["methods"])
    return res