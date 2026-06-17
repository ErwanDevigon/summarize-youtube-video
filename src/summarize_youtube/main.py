#!/usr/bin/env python3
import sys
from pathlib import Path
import subprocess
import re

from summarize_youtube.summarizer import LocalSummarizer


def main():
    print("🎥 summarize-yt — Transcript + Résumé IA (Gemma-4 12B)")
    print("=" * 65)

    # Récupération de l'URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("\nColle l'URL YouTube ici :\n> ").strip()

    if not url:
        print("❌ Aucune URL fournie.")
        sys.exit(1)

    # === Dossier de sortie ===
    output_dir = Path("~/Downloads/transcripts").expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Fichiers seront sauvegardés dans : {output_dir}")

    # 1. Appel à youtube-clean-transcript
    print("\n📥 Récupération du transcript propre...")
    try:
        result = subprocess.run([
            "python", "-m", "youtube_transcript.main",
            "--url", url,
            "--output", str(output_dir)
        ], capture_output=True, text=True, check=True)

        print(result.stdout.strip())

        # Récupération du dernier fichier .txt créé
        txt_files = sorted(output_dir.glob("*.txt"), key=lambda f: f.stat().st_mtime, reverse=True)
        if not txt_files:
            print("❌ Aucun fichier transcript trouvé.")
            sys.exit(1)

        transcript_file = txt_files[0]
        title = transcript_file.stem
        transcript_text = transcript_file.read_text(encoding="utf-8")

    except subprocess.CalledProcessError as e:
        print("❌ Erreur pendant la récupération du transcript :")
        print(e.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur : {e}")
        sys.exit(1)

    # 2. Résumé avec Gemma-4
    print("\n🤖 Génération du résumé avec Gemma-4 12B...")
    summarizer = LocalSummarizer()
    summary = summarizer.summarize(transcript_text, title)

    summary_file = transcript_file.with_name(f"{transcript_file.stem} - Summary.txt")

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(f"# Résumé : {title}\n\n")
        f.write(summary)

    print(f"✅ Résumé sauvegardé → {summary_file.name}")
    print(f"📍 {summary_file}")
    print("\n🎉 Opération terminée !")


if __name__ == "__main__":
    main()