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
    >"""

FOOTER = "</office:document-content>"

class ReplacerTestCase(unittest.TestCase):
    def test_replace_text_p(self):
        input_xml = HEADER \
            + "<text:p>Before</text:p>" \
            + "<text:p text:style-name='code'>${test.cpp}</text:p>" \
            + "<text:p>After</text:p>" \
            + FOOTER
        tree = etree.fromstring(input_xml)

        expected_xml = HEADER \
            + "<text:p>Before</text:p>" \
            + "<text:p text:style-name='code'>line1</text:p>" \
            + "<text:p text:style-name='code'>line2</text:p>" \
            + "<text:p>After</text:p>" \
            + FOOTER
        expected_tree = etree.fromstring(expected_xml)

        dct = {"test.cpp": "line1\nline2"}

        replacer.replace_placeholders(tree, dct)

        self._compare_trees(tree, expected_tree)

    def test_replace_text_p_span(self):
        input_xml = HEADER \
            + "<text:p>Before</text:p>" \
            + "<text:p text:style-name='code'>" \
            +   "<text:span text:style-name='T4'>${test.cpp}</text:span>" \
            + "</text:p>" \
            + "<text:p>After</text:p>" \
            + FOOTER
        tree = etree.fromstring(input_xml)

        expected_xml = HEADER \
            + "<text:p>Before</text:p>" \
            + "<text:p text:style-name='code'>line1</text:p>" \
            + "<text:p text:style-name='code'>line2</text:p>" \
            + "<text:p>After</text:p>" \
            + FOOTER
        expected_tree = etree.fromstring(expected_xml)

        dct = {"test.cpp": "line1\nline2"}

        replacer.replace_placeholders(tree, dct)

        self._compare_trees(tree, expected_tree)

    def test_replace_text_soft_page_break(self):
        input_xml = HEADER \
            + "<text:p>Before</text:p>" \
            + "<text:p text:style-name='code'>" \
            +   "<text:soft-page-break/>${test.cpp}" \
            + "</text:p>" \
            + "<text:p>After</text:p>" \
            + FOOTER
        tree = etree.fromstring(input_xml)

        expected_xml = HEADER \
            + "<text:p>Before</text:p>" \
            + "<text:p text:style-name='code'>line1</text:p>" \
            + "<text:p text:style-name='code'>line2</text:p>" \
            + "<text:p>After</text:p>" \
            + FOOTER
        expected_tree = etree.fromstring(expected_xml)

        dct = {"test.cpp": "line1\nline2"}

        replacer.replace_placeholders(tree, dct)

        self._compare_trees(tree, expected_tree)

    def _compare_trees(self, output, expected):
        def dump(tree): return etree.tostring(tree)
        output_str = dump(output)
        expected_str = dump(expected)
        if output_str != expected_str:
            print "# Output"
            print output_str
            print
            print "# Expected"
            print expected_str
            print
        self.assertEqual(output_str, expected_str)
