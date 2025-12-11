#!/usr/bin/env python

# -----------------------------------------------------------------
# Copyright (C) 2025 Erwann Rogard
# Source repository: https://github.com/rogard/helpers.py
#
# Python code:
# Released under the GNU General Public License v3.0 or later
# See https://www.gnu.org/licenses/gpl-3.0.html
# -----------------------------------------------------------------

import os
import re
import sys

UNSAFE_INFIX = ".unsafe"

DEFAULT_COMMENT_SYMBOLS = {
    "py": "#",
    "python": "#",
    "js": "//",
    "javascript": "//",
    "ts": "//",
    "cpp": "//",
    "c": "//",
    "h": "//",
    "java": "//",
    "rb": "#",
    "sh": "#",
    "bash": "#",
    "tex": "%",
    "txt": "#",
    "md": "<!--",
}

def guess_comment_symbol(language: str) -> str:
    """Return the default comment symbol for a given language."""
    return DEFAULT_COMMENT_SYMBOLS.get(language.lower(), "#")

# Default infix for unsafe files
UNSAFE_INFIX = ".unsafe"

CENSOR_BEGIN_ANCHOR_TEMPLATE = "{comment} <censor>"
CENSOR_END_ANCHOR_TEMPLATE = "{comment} </censor>"

DEFAULT_COMMENT_SYMBOLS = {
    "py": "#",
    "python": "#",
    "js": "//",
    "javascript": "//",
    "ts": "//",
    "cpp": "//",
    "c": "//",
    "h": "//",
    "java": "//",
    "rb": "#",
    "sh": "#",
    "bash": "#",
    "tex": "%",
    "txt": "#",
    "md": "<!--",
}

def guess_comment_symbol(language: str) -> str:
    return DEFAULT_COMMENT_SYMBOLS.get(language.lower(), "#")

def infer_output_path(input_path: str, infix: str) -> str:
    """
    Strip the first occurrence of `infix` from the filename.
    Raise ValueError if `infix` is not found.
    """
    base, ext = os.path.splitext(input_path)
    if infix not in base:
        raise ValueError(f"Input file '{input_path}' does not contain the required infix '{infix}'")
    cleaned_base = base.replace(infix, "", 1)
    return cleaned_base + ext

def process_file(*, input_path, output_path=None, language=None,
                 comment_symbol=None, search_begin=None,
                 search_end=None, replace_fn=None, infix=UNSAFE_INFIX):
    """
    Process a file by replacing text between <censor> anchors.
    All parameters are keyword-only.

    output_path:
        - None: auto-infer from input_path by removing `infix`
        - "-": print to stdout
        - sys.stdout: print to stdout
        - string: path to output file
    """
    # Compute output_path if not provided
    if output_path is None:
        output_path = infer_output_path(input_path, infix=infix)

    # Compute language from extension
    if language is None:
        ext = os.path.splitext(input_path)[1].lstrip(".")
        language = ext or "txt"

    # Compute comment_symbol
    if comment_symbol is None:
        comment_symbol = guess_comment_symbol(language)

    # Compute search anchors
    if search_begin is None:
        search_begin = CENSOR_BEGIN_ANCHOR_TEMPLATE.format(comment=comment_symbol)
        
    if search_end is None:
        search_end = CENSOR_END_ANCHOR_TEMPLATE.format(comment=comment_symbol)

    # Default replacement function
    if replace_fn is None:
        replace_fn = lambda: f"{comment_symbol} CENSORED"

    # Build regex pattern (non-greedy)
    pattern = re.compile(
        re.escape(search_begin) + r"(.*?)" + re.escape(search_end),
        flags=re.DOTALL
    )

    # Read input
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Replace censored blocks
    new_text = pattern.sub(lambda m: replace_fn(), text)

    # Write output
    if output_path == "-" or output_path is sys.stdout:
        print(new_text, end="")
        print(f"\n[INFO] Sanitized content printed to stdout.", file=sys.stderr)
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(new_text)
            print(f"Sanitized file written to: {output_path}")

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Sanitize a file by replacing <censor> blocks.")
    parser.add_argument("input_path", help="Path to the input file")
    parser.add_argument("-o", "--output_path", help="Output file path (use '-' for stdout)", default=None)
    parser.add_argument("-l", "--language", help="Language for comment symbol inference", default=None)
    parser.add_argument("-c", "--comment_symbol", help="Override comment symbol", default=None)
    parser.add_argument("--search_begin", help="Override <censor> begin anchor", default=None)
    parser.add_argument("--search_end", help="Override <censor> end anchor", default=None)
    parser.add_argument("--strip-infix", dest="infix", help="Infix marking unsafe file", default=UNSAFE_INFIX)

    args = parser.parse_args()

    # call the function
    process_file(
        input_path=args.input_path,
        output_path=args.output_path,
        language=args.language,
        comment_symbol=args.comment_symbol,
        search_begin=args.search_begin,
        search_end=args.search_end,
        infix=args.infix
    )
