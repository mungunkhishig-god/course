import re
import argparse
import unicodedata
from typing import Tuple

# Regex patterns
GOOGLE_RE = re.compile(r"^\d{3}-\d{3}-\d{4}$")  # e.g., 105-904-7569
YAHOO_RE  = re.compile(r"^\d+$")                # digits only
MSA_RE    = re.compile(r"^[A-Za-z]")           # starts with any letter

def clean_text(s: str) -> str:
    """Trim spaces and remove BOM if any"""
    return s.replace("\ufeff", "").strip()

def detect_service(text: str) -> Tuple[str, str]:
    """Return (service, reason)"""
    if GOOGLE_RE.match(text):
        return "google", "matched GOOGLE_RE"
    if YAHOO_RE.match(text):
        return "yahoo", "matched YAHOO_RE"
    if MSA_RE.match(text):
        return "msa", "starts with a letter (MSA rule)"
    return "unknown", "no pattern matched"

def debug_dump(raw: str, cleaned: str) -> None:
    print("=== DEBUG ===")
    print(f"Raw input (repr): {raw!r}")
    print(f"Cleaned input (repr): {cleaned!r}")
    if cleaned:
        first = cleaned[0]
        try:
            name = unicodedata.name(first)
        except ValueError:
            name = "<no name>"
        print(f"First char: '{first}'  code: U+{ord(first):04X}  name: {name}")
    print("=============\n")

def main():
    parser = argparse.ArgumentParser(description="Detect service from CLI argument and write to output.txt")
    parser.add_argument("id_string", help="The ID string to detect (e.g., 105-904-7569, 1079429, F107ZKKK)")
    parser.add_argument("-o", "--output", default="output.txt", help="Output file (default: output.txt)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    raw_input = args.id_string
    cleaned = clean_text(raw_input)

    if args.debug:
        debug_dump(raw_input, cleaned)

    service, reason = detect_service(cleaned)

    if args.debug:
        print(f"Detection result: {service} ({reason})")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(service)

if __name__ == "__main__":
    main()
