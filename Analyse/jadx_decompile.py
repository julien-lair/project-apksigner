import subprocess
def jadx_decompile(decompile = True):
    """
    Fonction permettant de décompiler avec jadx le .jar

    decompile : booleen permettant de décompiler ou non (utile si vous souhiatez pas decompiler à chaques éxécution)
    """
    if decompile:
        print("Décompilation du .jar avec jadx")
        cmd = [
            "jadx",
            "apksigner.jar",
            "-d", "decompile-json",
            "--output-format", "json",
            "--deobf"
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if(result.returncode == 0):
            print("Décompilation effectuée avec succès.")
        else:
            print("Une erreur est survenue lors de la décompilation de apksigner.jar")
            raise Exception("Erreur critique : décompilation impossible")
