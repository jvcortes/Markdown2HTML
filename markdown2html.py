#!/usr/bin/python3
"""
Markdown2HTML, generates an HTML file from a Markdown file.
"""
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: ./markdown2html.py README.md README.html",
            file=sys.stderr
        )
        exit(1)
    elif not os.path.exists(sys.argv[1]):
        print("Missing {}".format(sys.argv[1]), file=sys.stderr)
        exit(1)
    else:
        print(end='')
        exit(0)
