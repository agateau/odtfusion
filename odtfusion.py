#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
This file is part of the odtfusion project.

@author: Aurélien Gâteau <aurelien.gateau@free.fr>
@license: GPL v3 or later
"""
import os
import sys
from optparse import OptionParser

from odtfile import OdtFile
from textfilecache import TextFileCache
import replacer

USAGE = "%prog <odt-input-name> <odt-output-name> <txt-dir>"
DESCRIPTION = "Replace placeholders in a .odt file with the content of text files"

def main():
    parser = OptionParser(usage=USAGE, description=DESCRIPTION)
    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("Missing arguments")

    odt_input_name = args[0]
    odt_output_name = args[1]
    txt_dir = args[2]

    odt = OdtFile(odt_input_name)
    cache = TextFileCache(txt_dir)
    replacer.replace_placeholders(odt.tree, cache)
    odt.save(odt_output_name)

    return 0


if __name__=="__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
