import shutil
from zipfile import ZipFile

from lxml import etree

class OdtFile(object):
    __slots__= ["_input_name", "tree"]

    def __init__(self, name):
        self._input_name = name
        zip = ZipFile(name)
        content_file = zip.open("content.xml")
        self.tree = etree.parse(content_file)

    def save(self, name):
        assert self._input_name != name
        shutil.copy(self._input_name, name)
        with open("/tmp/content.xml", "w") as f:
            self.tree.write(f, encoding="utf-8")
        zip = ZipFile(name, "a")
        zip.write("/tmp/content.xml", "content.xml")
        zip.close()
