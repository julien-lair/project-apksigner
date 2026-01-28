from core.agent import call_agent_LLM
from tools.save import save_in_file
def macro_analyse(staticData):
    print("je fait une analyse macro")
    for data in staticData:
    
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
        res = call_agent_LLM(prompt)
        save_in_file("macro/"+ data["signature"]["name"]+".md", res)
