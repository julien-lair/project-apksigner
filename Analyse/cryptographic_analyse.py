from tqdm import tqdm 
import json
from core.agent import call_agent_LLM
def cryptographic_analyse(jsonData, process=True):
    
    totalCryptoMethod = get_total_crypto_method(jsonData)

    with tqdm(total=totalCryptoMethod, desc="Analyse cryptographique", unit="Méthode") as pbar:
        for classes in jsonData:

            for method in classes["methods"]:
                if method["category"] in ["cryptography","math"]:
                    #nous avons une méthode de crypto
                    code = ""
                    className = classes["signature"]["name"]
                    package = classes["signature"]["package"]
                    path = "decompile/decompile-json/sources/" + "/" +package.replace(".","/") + "/" + className.split(".")[-1] +".json"
                    
                    #Récupère le code de la méthode
                    with open(path, "r") as classesJson:
                        fileContent = json.loads(classesJson.read())
                    if fileContent != "":
                        for methodFile in fileContent["methods"]:
                            if methodFile["name"] == method["name"]:
                                #on est sur le bon bloc
                                code = methodFile["lines"]
                    if code != "":
                        #on a le code on peut lancer l'agent
                        prompt = """
You are a security-focused assistant specialized in cryptography. Analyze the following Java method's code in detail to detect cryptographic issues or weaknesses.

Task:
1. Identify all cryptographic primitives used in this method. Include:
   - Symmetric algorithms (AES, DES, ChaCha20, etc.)
   - Asymmetric algorithms (RSA, EC, DSA, etc.)
   - Hash functions (MD5, SHA-1, SHA-256, etc.)
   - Signature algorithms (RSAwithSHA256, ECDSA, etc.)
   - Random number generators

2. For each primitive, provide:
   - Algorithm name and type
   - Usage context (encryption, hashing, signature, key derivation, etc.)
   - Parameters used (key length, mode, IV, padding, salt, iterations, etc.)

3. Evaluate the usage against modern cryptographic best practices:
   - Correct key lengths?
   - Proper IV or nonce usage?
   - Adequate randomness (SecureRandom vs non-secure PRNG)?
   - Use of deprecated or weak algorithms (MD5, SHA-1, DES, ECB mode)?
   - Proper padding, salting, hashing, iterations for KDFs?

4. Provide a risk assessment:
   - List any detected weaknesses or misconfigurations
   - Provide recommendations for improvement
   - If usage appears secure, state clearly: "Nothing to report."

5. Output format: JSON, structured as follows:

{
  "method_name": "<method name>",
  "cryptography_findings": [
    {
      "algorithm": "<algorithm used>",
      "type": "<symmetric/asymmetric/hash/signature/random>",
      "usage": "<what it is used for>",
      "parameters": {
          "key_size": "<size in bits>",
          "mode": "<mode if applicable>",
          "iv": "<iv/nonce details>",
          "padding": "<padding scheme>",
          "salt": "<salt details>",
          "iterations": "<iterations if applicable>"
      },
      "risk": "<description of potential weakness>",
      "recommendation": "<how to fix or improve, or 'Nothing to report'>"
    },
    ...
  ]
}

Method code to analyze:""" + str(code)


                        if process:
                            res = call_agent_LLM(prompt,"qwen3:8b")
                            method["analyse_crypto"] = res

                        pbar.update(1) 
    return jsonData


def get_total_crypto_method(data):
    res = 0
    for elem in data:
        for method in elem["methods"]:
            if method["category"] in ["cryptography","math"]:
                res += 1
    return res