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

            if line == '\n':
                converted += '\n'
                continue

            result = transform(line)
            if result:
                converted += result + '\n'
        f.close()

    converted = transform_unordered_lists(converted)

    with open("{}".format(sys.argv[2]), 'w') as f:
        f.write(converted)
        f.close()


def transform(line):
    result = line

    match = re.search("^(\s{0,4}-\s)(.*)", line)
    if match:
        content = transform(match.group(2))
        result = list_element(content)

    match = re.search("^(#{1,6})\s(.*)", line)
    if match:
        header_level = len(match.group(1))
        result = header(match.group(2), header_level)

    return result

def transform_unordered_lists(file):
    converted = ""
    inside_list = False
    split = file.splitlines()

    for index, line in enumerate(split):

        result = line
        match = re.search("<uli>(.*)</uli>", line)
        if match:
            if not inside_list:
                inside_list = True
                result = "<ul>\n" + line
        elif not match:
            if inside_list:
                inside_list = False
                result = "</ul>\n" + line

        if index == len(split) - 1:
            if inside_list:
                inside_list = False
                result = result + "\n</ul>"

        converted += result + '\n'
    converted = converted.replace('<uli>', '<li>')
    converted = converted.replace('</uli>', '</li>')

    return converted


def header(line, header_level):
    return "<h{}>{}</h{}>".format(header_level, line, header_level)

def list_element(line):
    return "<uli>{}</uli>".format(line)


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
