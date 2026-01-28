from core.agent import call_agent_LLM
from tools.save import save_in_file
from tqdm import tqdm
def macro_analyse(staticData, process = True):
    print("je fait une analyse macro")
    print(f"total apelle à éffectué: {len(staticData)}")
    for data in tqdm(staticData, desc="Analyse macro", unit="class"):
    
        prompt = f"""
        This is a Java program packaged as a .jar, and I want to better understand the overall application. Please help me by analyzing the classes I provide.
        For each class, answer the following:
        Main purpose / role:
        What is the primary responsibility of this class? What does it do at a high level?
        Importance in the application:
        How important is this class within the application? Is it core, supporting, or auxiliary?
        Context and use case:
        In what context is this class used? What problem does it solve, and how does it fit into the overall program?
        Make reasonable assumptions if some details are missing.

        Here the informations about the class : 
        {data}
        """
        if process:
            res = call_agent_LLM(prompt)
            save_in_file("macro/"+ data["signature"]["name"]+".md", res)