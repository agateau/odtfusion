#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
This file is part of the odtfusion project.

@author: Aurélien Gâteau <aurelien.gateau@free.fr>
@license: GPL v3 or later
"""
import os
import re
import sys
from optparse import OptionParser

from lxml import etree

from odtfile import OdtFile
from textfilecache import TextFileCache

USAGE = "%prog <odt-input-name> <odt-output-name> <txt-dir>"
DESCRIPTION = "Replace placeholders in a .odt file with the content of text files"

TEXT_URI = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"

PLACEHOLDER_START = "${"
PLACEHOLDER_END = "}"
PLACEHOLDER_RX = re.compile("^" + re.escape(PLACEHOLDER_START) + "(.*)" + re.escape(PLACEHOLDER_END) + "$")

def replace_placeholders(tree, txt_dir):
    cache = TextFileCache(txt_dir)
    ns = {"text": TEXT_URI}
    for element in tree.xpath("//text:p", namespaces=ns):
        if element.text is None:
            continue
        result = PLACEHOLDER_RX.match(element.text)
        if result:
            name = os.path.join(txt_dir, result.group(1))
            print "Replacing %s" % name
            if name in cache:
                replace_placeholder(element, cache[name])
            else:
                print "ERROR: %s does not exist" % name

def replace_placeholder(element, content):
    # Remove ending lines
    content = content.rstrip()

    style = element.get("{%s}style-name" % TEXT_URI)
    first_pass = True
    for line in content.split("\n"):
        # Create next element, but not the first time: the first time we clear
        # the existing element (to remove the placeholder) and reuse it
        if first_pass:
            first_pass = False
            element.text = ""
        else:
            new_element = etree.Element("{%s}p" % TEXT_URI)
            new_element.set("{%s}style-name" % TEXT_URI, style)
            element.addnext(new_element)
            element = new_element

        # "parse" line
        content = line.lstrip()
        space_count = len(line) - len(content)

        # Insert content
        if space_count > 0:
            space_element = etree.Element("{%s}s" % TEXT_URI)
            space_element.set("{%s}c" % TEXT_URI, str(space_count))
            space_element.tail = content
            element.append(space_element)
        else:
            element.text = content

def main():
    parser = OptionParser(usage=USAGE, description=DESCRIPTION)
    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("Missing arguments")

    odt_input_name = args[0]
    odt_output_name = args[1]
    txt_dir = args[2]

    odt = OdtFile(odt_input_name)
    replace_placeholders(odt.tree, txt_dir)
    odt.save(odt_output_name)

    return 0


if __name__=="__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
