import requests
import json
from pathlib import Path

class LocalSummarizer:
    def __init__(self, base_url: str = "http://localhost:8080/v1"):
        self.base_url = base_url.rstrip("/")

    def summarize(self, transcript: str, title: str) -> str:
        prompt = f"""Tu es un excellent analyste technique. Fais un résumé clair, structuré et professionnel du transcript suivant.

**Règles :**
- Utilise des titres et des puces pour une excellente lisibilité
- Mets en avant : tracks du hackathon, sponsors + modèles/prizes, règles importantes, ressources offertes
- Sois concis mais complet

Vidéo : {title}

Transcript :
{transcript[:28000]}"""

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": "gemma4",
                    "messages": [
                        {"role": "system", "content": "Tu es un assistant technique précis et structuré."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2048
                },
                timeout=180
            )

            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"Erreur {response.status_code}: {response.text}"
        except requests.exceptions.ConnectionError:
            return "❌ Impossible de se connecter à llama-server.\nLance-le avec la commande : lma"
        except Exception as e:
            return f"Erreur lors du résumé : {e}"