import os
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = "REMOVED_API_KEY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

print("=== Modèles disponibles ===\n")

for model in genai.list_models():
    # On filtre pour voir les modèles d'embedding
    if "embed" in model.name.lower():
        print(f"- {model.name}")
        print(f"  Méthodes supportées: {model.supported_generation_methods}")
        print()
