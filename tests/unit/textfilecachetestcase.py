# -*- coding: UTF-8 -*-
"""
This file is part of the odtfusion project.

@author: Aurélien Gâteau <aurelien.gateau@free.fr>
@license: GPL v3 or later
"""
import os
import shutil
import tempfile
import unittest

from StringIO import StringIO

from textfilecache import _split_file, TextFileCache

HELLO = """
/// 1
Hello
/// 2
World
"""

class TextFileCacheTestCase(unittest.TestCase):
    def setUp(self):
        self.sb_dir = tempfile.mkdtemp(prefix="sandbox-", dir=".")
        full_path = os.path.join(self.sb_dir, "hello")
        open(full_path, "w").write(HELLO)

    def tearDown(self):
        shutil.rmtree(self.sb_dir)

    def test_split_file(self):
        fl = StringIO(HELLO)
        dct = _split_file(fl)
        self.assertEqual(len(dct), 2)
        self.assertEqual(dct["1"], "Hello\n")
        self.assertEqual(dct["2"], "World\n")

    def test_has_key(self):
        cache = TextFileCache(self.sb_dir)
        self.assert_("hello" in cache)
        self.assert_("hello#1" in cache)
        self.assert_("hello#2" in cache)
        self.assert_(not "hello#3" in cache)
