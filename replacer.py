# -*- coding: UTF-8 -*-
"""
This file is part of the odtfusion project.

@author: Aurélien Gâteau <aurelien.gateau@free.fr>
@license: GPL v3 or later
"""
import re

from lxml import etree

TEXT_URI = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"

PLACEHOLDER_START = "${"
PLACEHOLDER_END = "}"
PLACEHOLDER_RX = re.compile("^" + re.escape(PLACEHOLDER_START) + "(.*)" + re.escape(PLACEHOLDER_END) + "$")

def replace_placeholders(tree, dct):
    def do_replace(element, eat_span=False):
        result = None
        # placeholder can be either the text of an element, as in:
        #
        #   <text:p>${file.cpp}</text:p>"
        #
        # or there can be a soft-page-break element in:
        #
        #   <text:p>
        #       <text:soft-page-break/>
        #       ${file.cpp}
        #   </text:p>
        #
        #
        if element.text is not None:
            result = PLACEHOLDER_RX.match(element.text)
        else:
            page_break = element.find("{%s}soft-page-break" % TEXT_URI)
            if page_break is not None:
                result = PLACEHOLDER_RX.match(page_break.tail)
        if not result:
            return

        name = result.group(1)
        print "Replacing %s" % name
        if not name in dct:
            print "ERROR: %s does not exist" % name
            return

        if eat_span:
            placeholder_element = element.getparent()
        else:
            placeholder_element = element
        style = placeholder_element.get("{%s}style-name" % TEXT_URI)

        insert_content(placeholder_element, style, dct[name])
        placeholder_element.getparent().remove(placeholder_element)

    ns = {"text": TEXT_URI}

    for element in tree.xpath("//text:p", namespaces=ns):
        do_replace(element)

    for element in tree.xpath("//text:p/text:span", namespaces=ns):
        do_replace(element, eat_span=True)

def insert_content(previous_element, style, content):
    # Remove ending lines
    content = content.rstrip()

    for line in content.split("\n"):
        element = etree.Element("{%s}p" % TEXT_URI)
        element.set("{%s}style-name" % TEXT_URI, style)

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

        previous_element.addnext(element)
        previous_element = element
