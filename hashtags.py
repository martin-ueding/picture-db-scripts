#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

import re

class Tag(object):
    def __init__(self, text):
        """
        @param text: Human readable text.
        """
        self.text = text

    @staticmethod
    def from_encoded(encoded):
        return Tag(re.sub(r"_", " ", encoded))

    def encode(self):
        return re.sub(" ", "_", self.text)

    def __str__(self):
        return self.text

    def __repr__(self):
        return "Tag('%s')" % self.text

    def __lt__(self, other):
        return self.text < other.text

    def __eq__(self, other):
        return self.text == other.text


def parse_filename(name):
    """
    Parses the filename to find the hashtags.

    @param name: Filename with tags.
    @type name: str
    @return: Filename, list with tags.
    @rtype: tuple
    """
    m = re.match(r"([^#]+)(#.*)+(\.\w+)", name)

    result = []
    filename = name

    if not m is None:
        taglist = m.group(2).split("#")

        for tag in taglist:
            if len(tag) > 0:
                result.append(Tag.from_encoded(tag))

        filename = m.group(1)+m.group(3)

    return filename, result


def generate_filename(filename, tags):
    m = re.match(r"([^.]+)(\.\w+)", filename)

    if not m is None:
        name = m.group(1)
        suffix = m.group(2)

        if len(tags) == 0:
            taglist = ""
        else:
            taglist = "#"+"#".join(sorted(set([tag.encode() for tag in tags])))

        return name+taglist+suffix
