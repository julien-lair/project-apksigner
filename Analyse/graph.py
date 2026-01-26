import os
from igraph import Graph, plot
PATH = "../apksigner/sources/com/android/apksig"

def analyse_file_import(path, g : Graph):
    compteur = 0
    android_path = path.replace("/",".").split("com")
    if len(android_path) >= 1:
        android_path = "com"+android_path[1]
    else:
        print("erreur dans le nom de fichier")
        return
    g.add_vertices(android_path)
    with open(path,"r") as file:
        for line in file:
            if line.startswith("import"):
                compteur = 0
                importFile = line.split("import")[1].strip()
                if not importFile in g.vs["name"]:
                    g.add_vertices(importFile)
                g.add_edges([(android_path, importFile)])
            else:
                compteur += 1
                if compteur > 10:
                    break

def analyse_file(path, g):
    for fileName in os.listdir(path):
        full_path = os.path.join(path, fileName)
        if os.path.isfile(full_path):
            analyse_file_import(full_path,g)
            continue

        elif os.path.isdir(full_path):
            analyse_file(full_path,g)
            continue

# Création d'un graphe dirigé
g = Graph(directed=True)
analyse_file(PATH, g)
# On récupère les degrées sortant de chaques node     
in_degrees = g.indegree()
out_degrees = g.outdegree()
# On save sous forme n° node, degree
degree_index = []
for i in range(len(in_degrees)):
    degree_index.append((i,out_degrees[i]-in_degrees[i]))
#On trie les par rapport au degre >= 0
sorted_degree = sorted([x for x in degree_index if x[1] >= 0], key=lambda x: x[1], reverse=True)


print("les fonctions les plus importante (possiblement les plus importante) sont : ")
for i in sorted_degree:
    id,degree = i 
    print(f"{g.vs[id]["name"]} - deg: {degree}")

