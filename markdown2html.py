#!/usr/bin/python3
"""
Markdown2HTML, generates an HTML file from a Markdown file.
"""
import os
import re
import sys

def read_file(file):
    converted = ""

    with open(file) as f:
        for line in f:
            result = transform(line)
            if (result):
                converted += result + '\n'
        f.close()

    with open("{}".format(sys.argv[2]), 'w') as f:
        f.write(converted)
        f.close()


def transform(line):
    result = line

    match = re.search("^(#{1,6})\W(.*)", line)
    if match:
        header_level = len(match.group(1))
        result = header(match.group(2), header_level)

    return result


def header(line, header_level):
    return "<h{}>{}</h{}>".format(header_level, line, header_level)


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
        read_file(sys.argv[1])
        exit(0)
