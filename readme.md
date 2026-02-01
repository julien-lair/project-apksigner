# Commande pour installer les models
curl -fsSL https://ollama.com/install.sh | sh
pkill ollama
ollama pull qwen3-vl:32b
ollama pull qwen3:32b
echo $OPEN_BUTTON_TOKEN




# Comparatif des models
## Analyse model glm-4.7-flash:bf16:
+ consome peu de GPU
- beaucoup de RAM nécéssaire, prendre plutôt un model avec poid faible 

STATS :
- 60GB
- RAM: 90Go minimum
- NVIDIA GeForce RTX 5090 : utilisation à 4% = 1.27 Go (100% = 31.8Gb)

## Analyse model qwen3-vl:32b:
+ assez rapide 

STATS :
- 26 Gb stockage
- RAM: 28 Go min 
- NVIDIA GeForce RTX 5090 à 28,94 Gb/31.8gb utilisé par model

TEMPS:
- Analyse macro : 50s/class
- Analyse méthodes : 12.48s/method
- Analyse crypto: X

## Analyse model qwen3:8b
+ assez rapide

STATS :
- 26 Gb stockage
- RAM: 33 Go min 
- NVIDIA GeForce RTX 5090 à 28,6 Gb/31.8gb utilisé par model

TEMPS:
- Analyse crypto : 4s/method
