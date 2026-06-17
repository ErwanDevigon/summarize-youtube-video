# summarize-youtube-video

**Transcript propre + Résumé intelligent par IA locale**

Un outil en ligne de commande qui :
- Récupère les sous-titres auto-générés d’une vidéo YouTube
- Les nettoie parfaitement (grâce à [youtube-clean-transcript](https://github.com/ErwanDevigon/youtube-clean-transcript))
- Génère un **résumé structuré et pertinent** avec **Gemma-4 12B** (via llama.cpp)

---

## ✨ Fonctionnalités

- Utilisation de ton package `youtube-clean-transcript`
- Résumé automatique avec modèle local (aucun coût API)
- Sauvegarde dans `~/Downloads/transcripts/`
- Deux fichiers générés :
  - `Titre de la vidéo.txt` → Transcript complet et propre
  - `Titre de la vidéo - Summary.txt` → Résumé bien structuré
- Interface simple (CLI)

---

## Prérequis

- Python 3.10+
- [llama.cpp](https://github.com/ggerganov/llama.cpp) avec `llama-server` lancé sur le port 8080
- Ton alias `lma` pour lancer Gemma-4 12B
- `youtube-clean-transcript` installé en mode editable

---

## Installation

```bash
cd ~/Projets/summarize-youtube-video
pip install -e .

