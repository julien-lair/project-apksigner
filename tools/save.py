def save_in_file(name,content):
    with open("db/"+name, "w") as file:
        file.write(content)