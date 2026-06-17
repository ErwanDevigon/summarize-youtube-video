# summarize-youtube-video

**Transcript propre + Résumé intelligent par IA locale**

Un outil en ligne de commande simple qui permet de :

- Récupérer les sous-titres auto-générés d’une vidéo YouTube
- Les nettoyer parfaitement
- Générer un **résumé structuré et pertinent** avec un modèle local (Gemma-4 12B via llama.cpp)

---

## ✨ Fonctionnalités

- Utilise le package [`youtube-clean-transcript`](https://github.com/ErwanDevigon/youtube-clean-transcript)
- Résumé automatique avec un modèle local (aucun coût d’API)
- Sauvegarde automatique des fichiers dans `~/Downloads/transcripts/`
- Deux fichiers générés pour chaque vidéo :
  - `Titre de la vidéo.txt` → Transcript complet et propre
  - `Titre de la vidéo - Summary.txt` → Résumé bien structuré avec titres et puces

---

## Prérequis

- Python 3.10+
- [llama.cpp](https://github.com/ggerganov/llama.cpp) compilé avec `llama-server`
- Un modèle compatible (ex: Gemma-4 12B) chargé sur le port 8080
- `youtube-clean-transcript` installé

---

## Installation

```bash
git clone https://github.com/ErwanDevigon/summarize-youtube-video.git
cd summarize-youtube-video
pip install -e .
```

### Alias recommandé (facultatif)

Ajoutez dans votre `~/.bashrc` ou `~/.zshrc` :

```bash
summarize-yt() {
    cd ~/Downloads
    summarize-yt "$@"
}
```

Puis rechargez votre shell :
```bash
source ~/.bashrc
```

---

## Utilisation

```bash
# Mode interactif (recommandé)
summarize-yt
```

# Ou directement avec une URL
```bash
summarize-yt "https://www.youtube.com/watch?v=7otgeJXailY"
```

---

## Exemple de sortie

```
🎥 summarize-yt — Transcript + Résumé IA (Gemma-4 12B)
============================================================

📁 Fichiers seront sauvegardés dans : /home/user/Downloads/transcripts

📥 Récupération du transcript propre...
✅ Transcript sauvegardé → video name.txt

🤖 Génération du résumé avec Gemma-4 12B...
✅ Résumé sauvegardé → video name - Summary.txt
```

---

## Structure du projet

```
summarize-youtube-video/
├── src/summarize_youtube/
│   ├── main.py
│   └── summarizer.py
├── pyproject.toml
├── README.md
└── ...
```

---

## Licence

MIT License

---

**Auteur :** Erwan Devigon

