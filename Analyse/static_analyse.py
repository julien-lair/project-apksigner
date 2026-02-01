import json
from core.conf import DEEP_ANALYSE
def static_analysis(struct_json):
    """
    Fonction qui analyse le programme de chaques strcutures du programmes passer en param 
    """
    coefMin = 70
    if DEEP_ANALYSE:
        coefMin = 5 #ajuster ici pour sélectionner plus où moins de fichier a analyser (en %) 
    resAnalysis = []
    for i in range(len(struct_json)):
        if struct_json[i]["coef"] >= coefMin:
            jsonPath = struct_json[i]["json_path"]
            in_degree = struct_json[i]["nbr_degree_in"]
            res = static_analysis_file(jsonPath,in_degree)
            resAnalysis.append(res)
    return resAnalysis

def static_analysis_file(path, in_degree = 0):
    fileContent = ""
    resData = {}
    with open(path, "r") as jsonFile:
        fileContent = json.loads(jsonFile.read())
    if fileContent != "": #si le contenue du fichier n'est pas vide
        #On récupère plusieurs partie qui nous intérèsse 

        # Signature de la classe
        signature = {
            "package" : get_value_of_key(fileContent, "package"),
            "type" : get_value_of_key(fileContent, "type"),
            "implements" : get_value_of_key(fileContent, "implements"),
            "extends" : get_value_of_key(fileContent, "extends"),
            "name" : get_value_of_key(fileContent, "name"),
            "declaration" : get_value_of_key(fileContent, "declaration").split("\n")[-1],
            "in_degree" : in_degree
        }
        resData["signature"] = signature

        # fields 
        fields_value = get_value_of_key(fileContent, "fields")
        fields_array = []
        if fields_value:
            for field in fields_value:
                fields_array.append(field["declaration"].split("\n")[-1])

        resData["fields"] = fields_array

        # signature des méthodes
        methods_value = get_value_of_key(fileContent, "methods")
        methods_array = []
        if methods_value:
            for method in methods_value:
                if "/* synthetic */" in method["declaration"]:
                    # on passe les méthode synthétique (viens du compilateur)
                    continue
                tmp = {
                    "name": method["name"],
                    "return-type": method["return-type"],
                    "arguments": method["arguments"],
                    "declaration": method["declaration"]
                }
                # NOTE : si besoin d'une fonction de (IA function calling) get_corpMéthode() ici récupérer la clé "lines": contient les lignes de codes
                methods_array.append(tmp)

        resData["methods"] = methods_array
        

    return resData

def get_value_of_key(json, key):
    try:
        if json[key]:
            return json[key]
    except KeyError:
        return ""