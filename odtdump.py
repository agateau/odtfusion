#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
This file is part of the odtfusion project.

@author: Aurélien Gâteau <aurelien.gateau@free.fr>
@license: GPL v3 or later
"""
import sys
from optparse import OptionParser

from odtfile import OdtFile

USAGE = "%prog <odt-file-name>"
DESCRIPTION = "Dumps an indented version of the content.xml of a .odt file to stdout."

def main():
    parser = OptionParser(usage=USAGE, description=DESCRIPTION)
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Missing arguments")

    odt_name = args[0]
    odt = OdtFile(odt_name)
    odt.tree.write(sys.stdout, pretty_print=True)

    return 0


if __name__=="__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
