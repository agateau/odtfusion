import os
import shutil
from zipfile import ZipFile

from lxml import etree

TEXT_URI = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"

class OdtFile(object):
    def __init__(self, name):
        self.input_name = name
        zip = ZipFile(name)
        content_file = zip.open("content.xml")
        self.tree = etree.parse(content_file)

    def replace_placeholders(self, txt_dir):
        ns = {"text": TEXT_URI}
        for element in self.tree.xpath("//text:p", namespaces=ns):
            txt = element.text
            if txt is not None and txt.startswith("[") and txt.endswith("]"):
                name = os.path.join(txt_dir, txt[1:-1])
                if os.path.exists(name):
                    print "Replacing %s" % name
                    self._replace_placeholder(element, name)

    def _replace_placeholder(self, element, name):
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

    def save(self, name):
        assert self.input_name != name
        shutil.copy(self.input_name, name)
        with open("/tmp/content.xml", "w") as f:
            self.tree.write(f, encoding="utf-8")
        zip = ZipFile(name, "a")
        zip.write("/tmp/content.xml", "content.xml")
        zip.close()
