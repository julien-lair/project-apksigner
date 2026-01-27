import os
from igraph import Graph, plot
import json
PATH = "../decompile-json/sources/"

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
            return #le fihcier ne contient pas d'imports
        except Exception:
            print("Erreur lors de l'ouverture du fichier "+path) 



g = Graph(directed=True)

#Parser le json pour récupérer les classes.json
try:
    with open(PATH+"mapping.json","r") as mappingFile:
        mappingJson = json.loads(mappingFile.read())
except FileNotFoundError:
    print("Une erreur c'est produite lors de la lecture du programme. Vérifier l'existance du fichier sources/mapping.json")
if mappingJson:
    for i in range(len(mappingJson["classes"])):
        classPath = mappingJson["classes"][i]["json"]
        className = classPath.replace("/",".")
        classFullPath = PATH + classPath
        #on analyse le simport de chaques fichier
        generated_import_graph(classFullPath,className, g)

# On récupère les degrées sortant de chaques node     
in_degrees = g.indegree()
out_degrees = g.outdegree()
# On save sous forme n° node, degree
degree_index = []
for i in range(len(in_degrees)):
    degree_index.append((i,out_degrees[i]-in_degrees[i]))
#On trie les par rapport au degre >= 0
sorted_degree = sorted([x for x in degree_index if x[1] > 0], key=lambda x: x[1])

print("les fonctions les plus importante (possiblement les plus importante) sont : ")
for i in sorted_degree:
    id,degree = i 
    print(f"{g.vs[id]["name"]} - deg: {degree}")
