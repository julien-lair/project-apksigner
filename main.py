from Analyse.jadx_decompile import jadx_decompile
from Analyse.detection_classes import detect_core_class
from Analyse.static_analyse import static_analysis
from Analyse.macro_analyse import macro_analyse
from Analyse.structure_analyse import structure_analyse
from Analyse.deep_analyse import deep_analyse
from Analyse.cryptographic_analyse import cryptographic_analyse
from Analyse.vulnerability_analyse import vulnerability_analyse
from Analyse.double_check import verification_doubleCheck
from Analyse.synthese import synthese
from tools.save import save_in_file
DEBUG = True
import os, json
if __name__ == "__main__":
    os.system('clear')
    dir = "decompile-json"
    jadx_decompile(not DEBUG)
    coreClass = detect_core_class()
    staticData = static_analysis(coreClass)
    save_in_file("staticData.json",json.dumps(staticData, indent=2))
    macro_analyse(staticData, not DEBUG)
    methods_analysis = structure_analyse(staticData)
    save_in_file("methods_analysis.json",json.dumps(methods_analysis, indent=2))
    
    # cryptographic_analyse()
    # vulnerability_analyse()
    # synthese()