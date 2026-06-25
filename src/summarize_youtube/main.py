#!/usr/bin/env python3
"""
rezmyt — YouTube Transcript + Local AI Summary (v2.2)
"""

import sys
import argparse
from pathlib import Path
import subprocess

from summarize_me_this_text.summarizer import LocalSummarizer
from summarize_me_this_text.llama_server_manager import LlamaServerManager


def parse_args():
    parser = argparse.ArgumentParser(
        description="rezmyt — Clean YouTube transcript + local AI summary",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("url", nargs="?", help="YouTube URL to summarize")
    parser.add_argument("-s", "--style", 
                        choices=["structured", "bullets", "concise", "detailed", "transcript"],
                        help="Summary style. If omitted, generates all 3 versions")
    parser.add_argument("-l", "--lang", choices=["fr", "en"], default="fr",
                        help="Language of the summary (default: fr)")
    parser.add_argument("-o", "--output", type=Path, default=Path("~/transcripts").expanduser(),
                        help="Output directory")
    parser.add_argument("--keep-server", action="store_true",
                        help="Do not stop llama-server after summary")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("🎥 rezmyt — YouTube Transcript + Local AI Summary")
    print("=" * 72)

    # === URL handling ===
    if not args.url:
        args.url = input("\n📎 Paste YouTube URL:\n> ").strip()

    if not args.url:
        print("❌ No URL provided.")
        sys.exit(1)

    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)
    print(f"📁 Saving to: {args.output}")
    print(f"   Language: {args.lang}")
    if args.style:
        print(f"   Style   : {args.style} (single)")
    else:
        print(f"   Style   : ALL 3 (detailed + structured + bullets)")
    print()

    # 1. Fetch transcript
    print("📥 Fetching clean transcript...")
    try:
        result = subprocess.run(
            [
                "python", "-m", "youtube_transcript.main",
                "--url", args.url,
                "--output", str(args.output)
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=180
        )

        # === Extraction du nom du fichier créé ===
        transcript_file = None
        for line in result.stdout.splitlines():
            if "===TRANSCRIPT_FILE:" in line:
                file_path = line.split("===TRANSCRIPT_FILE:")[1].strip("= ")
                transcript_file = Path(file_path)
                break

        if not transcript_file or not transcript_file.exists():
            txt_files = sorted(
                args.output.glob("*.txt"),
                key=lambda f: f.stat().st_mtime,
                reverse=True
            )
            transcript_file = txt_files[0] if txt_files else None

        if not transcript_file:
            print("❌ No transcript file found.")
            sys.exit(1)

        title = transcript_file.stem
        transcript_text = transcript_file.read_text(encoding="utf-8")
        print(f"   ✅ Transcript loaded: {transcript_file.name}")

    except subprocess.CalledProcessError as e:
        print("❌ Failed to download transcript:")
        print(e.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error fetching transcript: {e}")
        sys.exit(1)
    
    # 2. Start server
    server_manager = LlamaServerManager()
    server_manager.start()
    
    # 3. Generate summary(s)
    summarizer = LocalSummarizer()

    if args.style:
        print(f"\n🤖 Generating {args.style} summary...")
        summaries = summarizer.summarize(transcript_text, title=title, language=args.lang)
        summaries = {args.style: summaries.get(args.style, "Error: style not generated")}
    else:
        print("\n🤖 Generating 3 summaries (detailed + structured + bullets)...")
        summaries = summarizer.summarize(transcript_text, title=title, language=args.lang)

    # 4. Save summary(s) with clickable URL
    for style, content in summaries.items():
        suffix = f" - {style.capitalize()} Summary" if not args.style else f" - Summary"
        summary_file = transcript_file.with_name(f"{title}{suffix} ({args.lang}).md")

        header = f"""# Summary: {title}

**Video:** [{title}]({args.url})
**URL:** {args.url}

**Style:** {style}
**Language:** {args.lang}
**Source:** {transcript_file.name}

---

"""

        summary_file.write_text(header + content, encoding="utf-8")
        print(f"✅ Saved → {summary_file.name}")

    # Cleanup
    if not args.keep_server:
        server_manager.stop_if_needed()
    else:
        print("🔄 Server kept running (--keep-server)")

    print("\n✅ Success !")
    print("🎉 Done!")


if __name__ == "__main__":
    main()
