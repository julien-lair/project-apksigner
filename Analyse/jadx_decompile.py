import subprocess
from core.conf import JAR_FILE
def jadx_decompile(decompile = True):
    """
    Fonction permettant de décompiler avec jadx le .jar

    decompile : booleen permettant de décompiler ou non (utile si vous souhiatez pas decompiler à chaques éxécution) Mode Debug
    """
    
    if decompile:
        print("Décompilation du .jar avec jadx")
        cmd = [
            "jadx",
            JAR_FILE,
            "-d", "decompile/decompile-json",
            "--output-format", "json",
            "--deobf"
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if(result.returncode != 0):
            print("Une erreur est survenue lors de la décompilation de apksigner.jar")
            raise Exception("Erreur critique : décompilation impossible")
        
        cmd = [
            "jadx",
           JAR_FILE,
            "-d", "decompile/decompile-java",
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
            print(f"Une erreur est survenue lors de la décompilation de {JAR_FILE}")
            raise Exception("Erreur critique : décompilation impossible")