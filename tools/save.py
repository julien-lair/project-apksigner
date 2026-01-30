import json
def save_in_file(name,content):
    with open("db/"+name, "w") as file:
        file.write(content)

def load_from_file(name):
    with open("db/"+name,"r") as file:
        return json.loads(file.read())