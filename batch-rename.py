#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

from PyQt4 import QtGui
import argparse
import json
import os
import picturedb
import sys

__docformat__ = "restructuredtext en"

class RenameButton(QtGui.QPushButton):
    def __init__(self, tag_text):
        super(RenameButton, self).__init__(tag_text)
        
        self.setAcceptDrops(True)
        self.tag_text = tag_text
        self.tag = picturedb.Tag(tag_text)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        local_files = [unicode(f.toLocalFile()).encode("utf8") for f in urls]

        self.handle_files(local_files)

    def handle_files(self, local_files):
        for file_ in local_files:
            self.handle_file(file_)

    def handle_file(self, file_):
        print("Adding {} to {}.".format(file_, self.tag_text))
        image = picturedb.Image(file_)
        image.add_tag(self.tag)
        image.save()


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.initUI()
        
    def initUI(self):
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        buttons = []
        with open(os.path.expanduser("~/.config/picture-db-scripts/favorite_tags.js")) as f:
            contents = f.read()
            tags = json.loads(contents)
        tags.sort()
        for tag in tags:
            vbox.addWidget(RenameButton(tag.encode("utf8")))
        self.setLayout(vbox)
        self.setWindowTitle("picture-db-scripts batch rename")

def main():
    options = _parse_args()

    app = QtGui.QApplication(sys.argv)

    ex = Example()
    ex.show()

    app.exec_()


def _parse_args():
    """
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description="")
    #parser.add_argument("args", metavar="N", type=str, nargs="*", help="Positional arguments.")
    #parser.add_argument("", dest="", type="", default=, help=)
    #parser.add_argument("--version", action="version", version="<the version>")

    return parser.parse_args()


if __name__ == "__main__":
    main()
