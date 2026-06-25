# rezmyt — YouTube Summary Tool v2.2

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![llama.cpp](https://img.shields.io/badge/llama.cpp-supported-brightgreen)](https://github.com/ggerganov/llama.cpp)

**Clean YouTube transcript + powerful local AI summaries.**

## Features

- Downloads clean YouTube transcripts (with timestamps in raw JSON)
- Generates **3 summaries by default** (Detailed + Structured + Bullets)
- Option to generate a single style with `--style`
- Saves video URL as clickable link in all summaries
- Creates rich metadata (`_info.json`)
- Fully local (powered by llama.cpp)

## Prerequisites

- Python 3.10+
- [llama.cpp](https://github.com/ggerganov/llama.cpp) with `llama-server`
- A good LLM model (Gemma-4, Llama-3.1, Mistral, Qwen, etc.)
- https://github.com/ErwanDevigon/youtube-clean-transcript
- https://github.com/ErwanDevigon/summarize-me-this-text

## Installation

```bash
# Clone the repositories
git clone https://github.com/ErwanDevigon/summarize-youtube-video.git
git clone https://github.com/ErwanDevigon/youtube-clean-transcript
git clone https://github.com/ErwanDevigon/summarize-me-this-text.git

# Install in editable mode
cd ~/Projets/summarize-me-this-text && pip install -e .
cd ~/Projets/youtube-clean-transcript && pip install -e .
cd ~/Projets/summarize-youtube-video && pip install -e .
```

## Usage

```bash
rezmyt https://youtu.be/v4F1gFy-hqg
rezmyt https://youtu.be/v4F1gFy-hqg -s bullets
rezmyt https://youtu.be/v4F1gFy-hqg -s detailed -l en
```

### Options

| Option           | Description |
|------------------|-----------|
| `URL`            | YouTube URL (positional or interactive) |
| `-s, --style`    | Summary style. If omitted → generates **3 versions** |
| `-l, --lang`     | Language (`fr` or `en`, default: `fr`) |
| `-o, --output`   | Output directory (default: `~/transcripts`) |
| `--keep-server`  | Do not stop the llama-server after running |

## Recommended Alias (add to `~/.bash_aliases` or `~/.zshrc`)

```bash
rezmyt() {
    local project_dir="$HOME/Projets/summarize-youtube-video"
    
    # Check if venv exists
    if [[ ! -d "$project_dir/venv" ]]; then
        echo "❌ Virtual environment not found for summarize-youtube-video."
        echo "   Please create it with:"
        echo "   cd $project_dir && python3 -m venv venv && source venv/bin/activate && pip install -e ."
        return 1
    fi

    # Run in a clean subshell
    (
        cd "$project_dir"
        source venv/bin/activate
        command rezmyt "$@"
    )
}
```

> After adding the alias, run `source ~/.bash_aliases` (or restart your terminal).

## Output Files

For each video you will get:

- `{title}.txt` — Clean readable transcript
- `{title}_raw.json` — Complete raw transcript
- `{title}_info.json` — Video metadata (URL, ID, title, date…)
- Three summary files:
  - `{title} - Detailed Summary (fr).md`
  - `{title} - Structured Summary (fr).md`
  - `{title} - Bullets Summary (fr).md`

All Markdown summaries contain a **clickable YouTube link** at the top.

---

**Ready to summarize!** 🚀

**Author:** Erwan Devigon

