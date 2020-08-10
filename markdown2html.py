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

            result = transform(line, False)
            if result:
                converted += result + '\n'
        f.close()

    converted = transform_unordered_lists(converted)
    converted = transform_ordered_lists(converted)
    converted = transform_paragraph_elements(converted)

    with open("{}".format(sys.argv[2]), 'w') as f:
        f.write(converted)
        f.close()


def transform(line, inside: bool):
    found = False
    result = line.rstrip()

    match = re.search("^(\s{0,4}-\s)(.*)", line)
    if match:
        found = True
        content = transform(match.group(2), True)
        result = unordered_list_element(content)

    match = re.search("^(\s{0,4}\*\s)(.*)", line)
    if match:
        found = True
        content = transform(match.group(2), True)
        result = ordered_list_element(content)

    match = re.search("^(#{1,6})\s(.*)", line)
    if match:
        found = True
        header_level = len(match.group(1))
        result = header(match.group(2), header_level)

    if found or inside:
        return result
    else:
        return paragraph_element(result)


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

def transform_ordered_lists(file):
    converted = ""
    inside_list = False
    split = file.splitlines()

    for index, line in enumerate(split):
        result = line
        match = re.search("<oli>(.*)</oli>", line)
        if match:
            if not inside_list:
                inside_list = True
                result = "<ol>\n" + line
        elif not match:
            if inside_list:
                inside_list = False
                result = "</ol>\n" + line

        if index == len(split) - 1:
            if inside_list:
                inside_list = False
                result += "\n</ol>"

        converted += result + '\n'
    converted = converted.replace('<oli>', '<li>')
    converted = converted.replace('</oli>', '</li>')

    return converted

def transform_paragraph_elements(file):
    converted = ""
    inside_paragraph = False
    split = file.splitlines()

    for index, line in enumerate(split):
        result = line
        match = re.search("<pe>(.*)</pe>", line)
        if match:
            if not inside_paragraph:
                inside_paragraph = True
                result = "<p>\n" + line
            if index < len(split) - 1 and re.search("<pe>(.*)</pe>", split[index + 1]):
                result = "{}<br/>".format(result)
        elif not match:
            if inside_paragraph:
                inside_paragraph = False
                result = "</p>\n" + line

        if index == len(split) - 1:
            if inside_paragraph:
                inside_paragraph = False
                result +="\n</p>"

        converted += result + '\n'
    converted = converted.replace('<pe>', '')
    converted = converted.replace('</pe>', '')

    return converted

def header(line, header_level):
    return "<h{}>{}</h{}>".format(header_level, line, header_level)

def unordered_list_element(line):
    return "<uli>{}</uli>".format(line)

def ordered_list_element(line):
    return "<oli>{}</oli>".format(line)

def paragraph_element(line):
    return "<pe>{}</pe>".format(line)


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
