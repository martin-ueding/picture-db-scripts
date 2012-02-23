#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

import re
import os.path

class Tag(object):
    def __init__(self, text):
        """
        @param text: Human readable text.
        """
        self.text = text

    @staticmethod
    def from_escaped(escaped):
        return Tag(re.sub(r"_", " ", escaped))

    def escape(self):
        escaped = re.sub(" ", "_", self.text)
        return escaped

    def __str__(self):
        return self.text

    def __repr__(self):
        return "Tag('%s')" % self.text

    def __lt__(self, other):
        return self.text < other.text

    def __eq__(self, other):
        return self.text == other.text


class Image(object):
    """
    basename: file name
    date: YYYYMMDD string
    dirname: folder name
    event: event name
    number: iterator number in image
    origname: original path
    prefix: combined date, event and number
    suffix: filetype
    """
    def __init__(self, filename):
        self.origname = filename
        self.dirname = os.path.dirname(filename)
        self.basename = os.path.basename(filename)

        self.parse_filename()
        self.parse_folder_name()

    def add_tag(self, tag):
        """
        @type tag: Tag
        @raise TypeError: Raised if not a hashtags.Tag given.
        """
        if not isinstance(tag, Tag):
            raise TypeError("Image::add_tag(hashtags.Tag)")

        self.tags.append(tag)

    def __repr__(self):
        return "Image(%s)" % self.current_path()

    def rename(self):
        os.rename(self.origname, self.current_path())

    def current_path(self):
        tagstring = ""
        if len(self.tags) > 0:
            tagstring = "#" + "#".join(sorted(set([tag.escape() for tag in self.tags])))

        filename = "%s-%s-%s%s.%s" % (self.date, self.event, self.number, tagstring, self.suffix)

        return os.path.join(os.path.dirname, filename)

    def parse_filename(self):
        """
        Parses the filename to find the hashtags.
        """
        m = re.match(r"([^#]+)(#.*)+(\.\w+)", self.basename)

        self.tags = []

        if not m is None:
            taglist = m.group(2).split("#")

            for tag in taglist:
                if len(tag) > 0:
                    self.tags.append(Tag.from_escaped(tag))

            self.prefix = m.group(1)
            nameparts = self.prefix.split('-')
            self.number = nameparts[2]

            self.suffix = m.group(3)

    def parse_folder_name(self):
        """
        Parses date and event name from a folder name.
        """
        pattern = re.compile(r"([12]\d{3}[01]\d[0123]\d)-([^/]+)/?")
        m = pattern.match(os.path.basename(self.dirname))
        if m is not None:
            self.date = m.group(1)
            self.event = m.group(2)
