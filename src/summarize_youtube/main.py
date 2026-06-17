#!/usr/bin/env python3
"""
rezmyt — YouTube Transcript + Local AI Summary (v2.0)
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
    parser.add_argument("-s", "--style", choices=["structured", "bullets", "concise", "detailed", "transcript"],
                        default="structured", help="Summary style")
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

    # === URL handling FIRST (before heavy server start) ===
    if not args.url:
        args.url = input("\n📎 Paste YouTube URL:\n> ").strip()

    if not args.url:
        print("❌ No URL provided.")
        sys.exit(1)

    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)
    print(f"📁 Saving to: {args.output}")
    print(f"   Style   : {args.style}")
    print(f"   Language: {args.lang}\n")

    # === Start server only now ===
    server_manager = LlamaServerManager()
    server_manager.start()

    # 1. Fetch transcript
    print("📥 Fetching clean transcript...")
    try:
        subprocess.run(
            [
                "python", "-m", "youtube_transcript.main",
                "--url", args.url,
                "--output", str(args.output)
            ],
            check=True
        )

        # Get latest .txt file
        txt_files = sorted(
            args.output.glob("*.txt"),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )

        if not txt_files:
            print("❌ No transcript found.")
            server_manager.stop_if_needed()
            sys.exit(1)

        transcript_file = txt_files[0]
        title = transcript_file.stem
        transcript_text = transcript_file.read_text(encoding="utf-8")

    except FileNotFoundError:
        print("❌ youtube-clean-transcript not found. Please install it in editable mode.")
        server_manager.stop_if_needed()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error fetching transcript: {e}")
        server_manager.stop_if_needed()
        sys.exit(1)

    # 2. Generate summary with full options
    print(f"\n🤖 Generating {args.style} summary in {args.lang}...")
    summarizer = LocalSummarizer()

    summary = summarizer.summarize(
        transcript_text,
        title=title,
        style=args.style,
        language=args.lang
    )

    # Save with nice filename (style + lang suffix like in summarize-me-this-text)
    suffix = f" [{args.style}]" if args.style != "structured" else ""
    summary_file = transcript_file.with_name(f"{title} - Summary{suffix} ({args.lang}).md")

    summary_file.write_text(
        f"# Summary: {title}\n"
        f"Style: {args.style} | Lang: {args.lang}\n\n"
        f"{summary}",
        encoding="utf-8"
    )

    print(f"✅ Summary saved → {summary_file.name}")

    # Cleanup
    if not args.keep_server:
        server_manager.stop_if_needed()
    else:
        print("🔄 Server kept running (--keep-server)")

    print("\n🎉 Done!")


if __name__ == "__main__":
    main()
