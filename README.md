# rezmyt — YouTube Summary Tool v2.0

Clean YouTube transcript + **local** AI summary (powered by `summarize-me-this-text`).

## Installation

```bash
# 1. Clone
git clone https://github.com/ErwanDevigon/summarize-youtube-video.git
cd summarize-youtube-video

# 2. Install dependencies
pip install -e .

# (Make sure youtube-clean-transcript is also installed in editable mode)
```

## Usage

```bash
rezmyt https://youtu.be/TNwJ1LMiENk
rezmyt https://youtu.be/TNwJ1LMiENk -s bullets
rezmyt https://youtu.be/TNwJ1LMiENk -s transcript -l en
```

### Options

- `URL` → positionnel ou interactif
- `-s, --style` → `structured` (défaut), `bullets`, `concise`, `detailed`, `transcript`
- `-l, --lang` → `fr` (défaut) ou `en`
- `-o, --output` → dossier de sortie (`~/transcripts` par défaut)
- `--keep-server` → ne pas arrêter le llama-server après utilisation

## Alias recommandé (dans `~/.bash_aliases`)

```bash
rezmyt() {
    mkdir -p ~/transcripts
    cd ~/transcripts
    echo "📁 Working directory: ~/transcripts"
    command rezmyt "$@"
}
```

