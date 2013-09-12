#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

import argparse
from PyQt4 import QtGui
import sys
import picturedb

__docformat__ = "restructuredtext en"

class RenameButton(QtGui.QPushButton):
    def __init__(self, tag_text, parent):
        super().__init__(tag_text, parent)
        
        self.setAcceptDrops(True)
        self.tag = picturedb.Tag(tag_text)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        print(urls)
        local_files = [f.toLocalFile() for f in urls]
        print(local_files)

        self.handle_files(local_files)

    def handle_files(self, local_files):
        for file_ in local_files:
            self.handle_file(file_)

    def handle_file(self, file_):
        image = picturedb.Image(file_)
        image.add_tag(self.tag)
        image.save()


class Example(QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        
    def initUI(self):
        button = RenameButton("Tag1", self)
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
