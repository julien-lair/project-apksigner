from Analyse.core_class import listCoreClass
import json
def analyse(repertoire):
    #lister les class essentiel au programme
    classCore = listCoreClass(repertoire)
    print(classCore[0]["class"])
    print(classCore[0]["json_path"])
    with open(classCore[0]["json_path"], "r") as ClassFile:
        jsonClassFile = json.loads(ClassFile.read())
    dataSelectedFromClass = {
        "fields":{
            "name" : "; ".join(field["name"] for field in jsonClassFile["fields"]),
        },
        "method" : {
            "methods" : "; ".join(f'{m["name"]}({", ".join(m["arguments"])})' for m in jsonClassFile["methods"])
        },
        "inner-classes" : {
            
        }

    }
    
    print(json.dumps(dataSelectedFromClass, indent=4))



if __name__ == "__main__":
    #jadx/bin/jadx apksigner.jar -d decompile-json --output-format json --cfg --deobf 
    dir = "decompile-json"
    analyse(dir)