#!/usr/bin/python3
"""
Markdown2HTML, generates an HTML file from a Markdown file.
"""
import hashlib
import os
import re
import sys


def generate_file(path):
    """
    Reads a Markdown file and converts its contents into a HTML file named
    after `sys.argv[2]`.

    Parameters:
        path (str): path to the file to convert
    """
    converted = ""

    with open(file) as f:
        for line in f:

            if line == '\n':
                converted += '\n'
                continue

            result = transform(line, False)
            if result:
                result = format_text(result)
                converted += result + '\n'

        f.close()

    converted = transform_unordered_lists(converted)
    converted = transform_ordered_lists(converted)
    converted = transform_paragraph_elements(converted)

    with open("{}".format(sys.argv[2]), 'w') as f:
        f.write(converted)
        f.close()


def transform_line(line, partial: bool):
    """
    Transforms a Markdown formatted string into HTML.

    Depending of its contents:
        - A line containing a header (starting with a '#' character) will be
        converted into a HTML header element (`<h1-6>`).
        - A line containing an unordered list element (starting with a '-'
        character) will be converted into an `<uli>` element.
        - A line containing an ordered list element (starting with a '*'
        character) will be converted into an `<oli>` element.
        - A line containing text that doesn't fit into the previous conditions
        will be converted into a `<pe>` element.

    Parameters:
        - line (str): Line to convert
        - partial (bool): Indicates when the function has to only convert a
            part of `line`
    """
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


def format_text(line):
    """
    Transforms a Markdown text formatted string into HTML text formatting.

    Depending of its contents:
        - Bold text (surrounded by two '*' characters) will
            be converted into a HTML `<b>` element.
        - Emphasis text (surrounded by two underscore
            characters) will be converted into a HTML `<em>` element.
        - Text surrounded by two levels of square bracket
            characters will be MD5 hashed.

    Parameters:
        - line (str): LIne to convert
    """
    result = line
    result = re.sub("\*\*(.*?)\*\*", r"<b>\1</b>", result)
    result = re.sub("__(.*?)__", r"<em>\1</em>", result)
    result = re.sub(
        "\[\[(.*?)\]\]",
        lambda match: hashlib.md5(match.group(1).encode()).hexdigest(),
        result
    )
    result = re.sub(
        "\(\((.*?)\)\)",
        lambda match: match.group(1).replace('c', '').replace('C', ''),
        result
    )

    return result


def transform_unordered_lists(file):
    """
    Surrounds `<uli>` elements inside an `<ul>` element, and converts them into
    `<li>` elements.

    Parameters:
        file (str): file contents to transform.
    """
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
    """
    Surrounds `<oli>` elements inside an `<ol>` element, and converts them into
    `<li>` elements.

    Parameters:
        file (str): file contents to transform
    """
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
    """
    Surrounds `<pe>` elements inside a `<p>` element, and converts them into
    tagless inline text.


    Parameters:
        file (str): file contents to transform
    """
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
    """
    Transforms a Markdown formatted line containing a header into a HTML header.

    Parameters:
        - line (str): line to transform
        - header_level (int): level for the transformed header,
            can be a value between 1 and 6.
    """
    return "<h{}>{}</h{}>".format(header_level, line, header_level)

def unordered_list_element(line):
    """
    Transforms a Markdown formatted line containing a unordered list element
    into an `<uli>` element, which will be later converted into a `<li>`
    element contained inside an `<ul>` element.

    Parameters:
        - line (str): line to transform
    """
    return "<uli>{}</uli>".format(line)

def ordered_list_element(line):
    """
    Transforms a Markdown formatted line containing a ordered list element
    into an `<uli>` element, which will be later converted into a `<li>`
    element contained inside an `<ol>` element.

    Parameters:
        - line (str): line to transform
    """
    return "<oli>{}</oli>".format(line)

def paragraph_element(line):
    """
    Transforms a line containing unformatted text into an `<pe>`
    element, which will be later converted into inline text surrounded by a
    `<p>` element.

    Parameters:
        - line (str): line to transform
    """
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
        generate_file(sys.argv[1])
        exit(0)
