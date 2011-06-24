#!/usr/bin/env python
import os
import sys
from optparse import OptionParser

from lxml import etree

from odtfile import OdtFile

USAGE="%prog <odt-input-name> <odt-output-name> <txt-dir>..."

TEXT_URI = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"

def replace_placeholders(tree, txt_dir):
    ns = {"text": TEXT_URI}
    for element in tree.xpath("//text:p", namespaces=ns):
        txt = element.text
        if txt is not None and txt.startswith("[") and txt.endswith("]"):
            name = os.path.join(txt_dir, txt[1:-1])
            print "Replacing %s" % name
            if os.path.exists(name):
                replace_placeholder(element, name)
            else:
                print "ERROR: %s does not exist" % name

def replace_placeholder(element, name):
    style = element.get("{%s}style-name" % TEXT_URI)
    first_pass = True
    for line in open(name).readlines():
        # Create next element, but not the first time: the first time we
        # reuse the existing element
        if first_pass:
            first_pass = False
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
            element.insert(0, space_element)
            space_element.tail = content
        else:
            element.text = content

def main():
    parser = OptionParser(usage=USAGE)

    # Add an option which takes an argument and is stored in options.filename.
    # 'metavar' is an example of argument and should match the text in 'help'.
    parser.add_option("-f", "--file", dest="filename",
                      help="write report to FILE", metavar="FILE")

    # Add a boolean option stored in options.verbose.
    parser.add_option("-x", "--xyz",
                      action="store_true", dest="xyz", default=True,
                      help="use 'xyz' method")

    # Add an invert boolean option stored in options.verbose.
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    (options, args) = parser.parse_args()

    if len(args) != 3:
        parser.error("Missing args")

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
