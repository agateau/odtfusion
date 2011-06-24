import shutil
from tempfile import NamedTemporaryFile
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
        with NamedTemporaryFile() as tempFile:
            self.tree.write(tempFile, encoding="utf-8")
            tempFile.flush()
            with ZipFile(name, "a") as zip:
                zip.write(tempFile.name, "content.xml")
# vi: ts=4 sw=4 et
