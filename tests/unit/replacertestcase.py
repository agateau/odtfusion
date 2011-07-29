# -*- coding: UTF-8 -*-
"""
This file is part of the odtfusion project.

@author: Aurélien Gâteau <aurelien.gateau@free.fr>
@license: GPL v3 or later
"""
import unittest

from lxml import etree

import replacer

HEADER = """
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    >
"""

FOOTER = "</office:document-content>"

class ReplacerTestCase(unittest.TestCase):
    def test_replace_textp(self):
        input_xml = HEADER \
            + "<text:p>${test.cpp}</text:p>" \
            + FOOTER
        tree = etree.fromstring(input_xml)

        expected_xml = HEADER \
            + "<text:p>hello</text:p>" \
            + FOOTER
        expected_tree = etree.fromstring(expected_xml)

        dct = {"test.cpp": "hello"}

        replacer.replace_placeholders(tree, dct)

        self._compare_trees(tree, expected_tree)

    def _compare_trees(self, output, expected):
        output_str = etree.tostring(output)
        expected_str = etree.tostring(expected)
        self.assertEqual(output_str, expected_str)
