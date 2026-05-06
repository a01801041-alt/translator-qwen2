#!/usr/bin/env python3
"""
cli.py — Command-line interface for the Qwen2-0.5B Translator.

Usage:
    python cli.py                          # interactive mode
    python cli.py --demo                   # run the 3 required demo phrases
    python cli.py -t "Hello" -s English -l Spanish
"""

import argparse
from translator import Translator


DEMO_PHRASES = [
    ("I like soccer",  "English", "Spanish"),
    ("How are you?",   "English", "Spanish"),
    ("What time is it?", "English", "Spanish"),
]


def run_demo(t: Translator) -> None:
    print("\n" + "=" * 55)
    print("  DEMO — 3 required example phrases")
    print("=" * 55)
    for text, src, tgt in DEMO_PHRASES:
        print(f"\n  [{src}] {text}")
        result = t.translate(text, src, tgt)
        print(f"  [{tgt}] {result}")
    print("\n" + "=" * 55 + "\n")


def interactive_mode(t: Translator) -> None:
    print("\nQwen2-0.5B Translator — interactive mode")
    print("Type 'quit' or 'exit' to stop.\n")
    while True:
        text = input("Text to translate: ").strip()
        if text.lower() in ("quit", "exit", "q"):
            break
        if not text:
            continue
        src = input("Source language [English]: ").strip() or "English"
        tgt = input("Target language [Spanish]: ").strip() or "Spanish"
        print(f"\n→ {t.translate(text, src, tgt)}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Translate text with Qwen2-0.5B")
    parser.add_argument("--demo", action="store_true", help="Run the 3 demo phrases and exit")
    parser.add_argument("-t", "--text", help="Text to translate")
    parser.add_argument("-s", "--source", default="English", help="Source language (default: English)")
    parser.add_argument("-l", "--lang", default="Spanish", help="Target language (default: Spanish)")
    args = parser.parse_args()

    print("Loading Qwen2-0.5B model…")
    t = Translator()
    print("Ready.\n")

    if args.demo:
        run_demo(t)
    elif args.text:
        result = t.translate(args.text, args.source, args.lang)
        print(f"[{args.lang}] {result}")
    else:
        interactive_mode(t)


if __name__ == "__main__":
    main()
