from Analyse.jadx_decompile import jadx_decompile
from Analyse.detection_classes import detect_core_class
from Analyse.static_analyse import static_analysis
from Analyse.macro_analyse import macro_analyse
from Analyse.structure_analyse import structure_analyse
from Analyse.cryptographic_analyse import cryptographic_analyse
from Analyse.vulnerability_analyse import vulnerability_analyse
from Analyse.synthese import synthese
from tools.save import save_in_file, load_from_file
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section
from core.conf import DEBUG
import os, json

if __name__ == "__main__":

    # 1 - décompilation
    jadx_decompile(not DEBUG)

    # 2 - Filtre pour récupérer classes pertinentes
    coreClass = detect_core_class()

    # 3 - Analyse static
    staticData = static_analysis(coreClass)
    if not DEBUG:
        save_in_file("staticData.json",json.dumps(staticData, indent=2)) #sauvegarde du fichier

    # 4 - Analyse macro : contexte
    macro_data = macro_analyse(staticData, not DEBUG)
    if not DEBUG:
        save_in_file("macro.json",json.dumps(staticData, indent=2))
    else:
        macro_data = load_from_file("macro.json")

    # 5 - Analyse structurelle : catégorise les méthodes
    methods_analysis = structure_analyse(macro_data, not DEBUG)
    if not DEBUG:
        save_in_file("methods_analysis.json",json.dumps(methods_analysis, indent=2))
    else:
        methods_analysis = load_from_file("methods_analysis.json")

    # 6 - Analyse crypto
    cryptoAnalysys = cryptographic_analyse(methods_analysis, not DEBUG)
    if not DEBUG:
        save_in_file("crypto_analyse.json",json.dumps(cryptoAnalysys, indent=2))
    else:
        cryptoAnalysys = load_from_file("crypto_analyse.json")

    # 7 - Analyse de vulns
    vulnAnalysis = vulnerability_analyse(cryptoAnalysys, not DEBUG)
    if not DEBUG:
        save_in_file("vulnerability.json",json.dumps(cryptoAnalysys, indent=2))
    else:
        vulnAnalysis = load_from_file("vulnerability.json")

    # 8 - Génération de rapport
    rapport = synthese(vulnAnalysis, not DEBUG)
    if DEBUG:
        with open("db/Security_Analysis_Report_2.md", "r") as file:
            rapport = file.read()

    # Enregistrement en pdf
    pdf = MarkdownPdf(
        toc_level=2,
        optimize=True
    )

    pdf.add_section(Section(rapport, toc=True))

    # Sauvegarde du PDF
    pdf.save("db/Security_Analysis_Report.pdf")

    print("Analyse terminé")
    print("\nRapport de synthèse généré : db/Security_Analysis_Report.pdf")
