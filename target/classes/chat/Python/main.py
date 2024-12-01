import os
import sys
import json
from dotenv import load_dotenv
import google.generativeai as gen_ai
import logging
import absl.logging

# Désactiver les logs inutiles de gRPC
logging.root.removeHandler(absl.logging._absl_handler)
absl.logging._warn_preinit_stderr = False
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_LOG_SEVERITY_LEVEL"] = "ERROR"

# Charger les variables d'environnement
load_dotenv()

# Configurer l'API Google Generative AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
else:
    print(json.dumps({"error": "Clé API non définie"}))
    sys.exit(1)

# Précharger le modèle
model = gen_ai.GenerativeModel('gemini-pro')
chat_session = model.start_chat(history=[])

def handle_request(user_input):
    try:
        # Envoyer la requête à Gemini-Pro
        response = chat_session.send_message(user_input)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}

def main():
    while True:
        # Lire l'entrée utilisateur depuis stdin
        user_input = sys.stdin.readline().strip()
        if not user_input:
            continue

        # Gérer la requête
        result = handle_request(user_input)

        # Écrire la réponse sur stdout
        print(json.dumps(result))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
