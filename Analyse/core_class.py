import os
from igraph import Graph
import json

def generated_import_graph(path, className, g : Graph):
    g.add_vertices(className)
    with open(path,"r") as classFile:
        classFileJson = json.loads(classFile.read())
    if classFileJson:
        try:
            for i in range(len(classFileJson["imports"])):
                importLine = classFileJson["imports"][i]
                #si il s'agit d'une classe interne à l'app (pas une class java.*)
                if importLine.startswith("com"):
                    #on vérifie si le noeud existe déjà 
                    if not importLine in g.vs["name"]:
                        g.add_vertices(importLine)
                    g.add_edges([(className, importLine)])
        except KeyError:
            return #le fichier ne contient pas d'imports
        except Exception:
            print("Erreur lors de l'ouverture du fichier "+path) 




def listCoreClass(repertoire):
    """    
    :param repertoire: répertoire des fichier décompiler avec jadx

    listCoreClass créer un graph des imports de fonction entre chaques class, 
    puis calcul les degrée de chaques noeud de graph pour déterminer les class centrale / coeur du système.
    """
    g = Graph(directed=True)
    path = repertoire+"/sources/"
    #Parser le json pour récupérer les classes.json
    try:
        with open(path+"mapping.json","r") as mappingFile:
            mappingJson = json.loads(mappingFile.read())
            if mappingJson:
                for i in range(len(mappingJson["classes"])):
                    classPath = mappingJson["classes"][i]["json"]
                    className = classPath.replace("/",".")
                    classFullPath = path + classPath
                    #on analyse les imports de chaques fichiers
                    generated_import_graph(classFullPath,className, g)
    except FileNotFoundError:
        print("Une erreur c'est produite lors de la lecture du programme. Vérifier l'existance du fichier sources/mapping.json")
    
    

    # On récupère les degrées sortant de chaques node     
    in_degrees = g.indegree()
    out_degrees = g.outdegree()

    # On sauvegarde sous forme n° node, degree
    max_degree = 0
    degree_index = []
    for i in range(len(in_degrees)):
        degree = out_degrees[i]-in_degrees[i]
        degree_index.append((i,degree))
        if degree > max_degree:
            max_degree = degree

    #On trie les par rapport au degre >= 0
    sorted_degree = sorted([x for x in degree_index if x[1] > 0], key=lambda x: x[1], reverse=True)

    coefImportance = 100 / max_degree
    classCore = []
    for i in sorted_degree:
        id,degree = i
        data = {
            "class": g.vs[id]["name"].split(".json")[0],
            "json_path": path+g.vs[id]["name"].replace(".","/").replace("/json",".json"),
            "import": {
                "degree": degree,
                "coef": round(degree * coefImportance, 2)
            }
        }
        classCore.append(data)
    return classCore