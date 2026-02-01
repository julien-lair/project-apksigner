import json
from igraph import Graph


def detect_core_class(repertoire = "decompile/decompile-json"):
    """    
    :param repertoire: répertoire des fichier décompiler avec jadx

    listCoreClass créer un graph des imports de fonction entre chaques classes, 
    puis calcul les degrées de chaques noeud de graph pour déterminer les classes pertinentes / coeur du système.
    """
    print("Recherche des classes pertinentes")

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
        print("Une erreur c'est produite lors de la lecture de mapping json. Vérifier l'existance du fichier sources/mapping.json")
        raise Exception("Erreur critique : fichier mapping.json introuvable")

    

    # On récupère les degrées sortant de chaques node     
    in_degrees = g.indegree()
    out_degrees = g.outdegree()

    # On sauvegarde sous forme n° node, degree
    max_degree = 0
    degree_index = []
    for i in range(len(in_degrees)):
        degree = out_degrees[i] + in_degrees[i]
        degree_index.append((i,degree))
        if degree > max_degree:
            max_degree = degree
    #On trie les par rapport au degre > 0
    sorted_degree = sorted([x for x in degree_index if x[1] > 0], key=lambda x: x[1], reverse=True)
    coefImportance = 100 / max_degree
    classCore = []
    for i in sorted_degree:
        id,degree = i
        NodeNameDegreeIn = []
        for n in g.neighbors(id, mode="IN"):
            name = g.vs[n]["name"]
            if name not in NodeNameDegreeIn:
                NodeNameDegreeIn.append(name)

        data = {
            "json_path": path+g.vs[id]["name"].replace(".","/").replace("/json",".json"),
            "coef": round(degree * coefImportance, 2),
            "nbr_degree_in" :NodeNameDegreeIn
        }
        classCore.append(data)
    
    
    return classCore

def generated_import_graph(path, className, g : Graph):
    g.add_vertices(className)
    with open(path,"r") as classFile:
        classFileJson = json.loads(classFile.read())
    if classFileJson:
        try:
            for i in range(len(classFileJson["imports"])):
                importLine = classFileJson["imports"][i]
                #si il s'agit d'un import interne à l'app (pas une class java.*)
                if importLine.startswith("com"):
                    #on vérifie si le noeud existe déjà 
                    importLine = importLine + ".json"
                    if not importLine in g.vs["name"]:
                        g.add_vertices(importLine)

                    g.add_edges([(className, importLine)])
        except KeyError:
            return #le fichier ne contient pas d'imports
        except Exception:
            print("Erreur lors de l'ouverture du fichier "+path) 
