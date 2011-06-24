#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
This file is part of the odtfusion project.

@author: Aurélien Gâteau <aurelien.gateau@free.fr>
@license: GPL v3 or later
"""
import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

from textfilecachetestcase import TextFileCacheTestCase

def main():
    unittest.main()

if __name__ == "__main__":
    main()
# vi: ts=4 sw=4 et
