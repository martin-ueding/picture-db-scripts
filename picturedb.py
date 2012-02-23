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

    def __init__(self, filename):
        self.basename = ""
        self.date = ""
        self.dirname = ""
        self.event = ""
        self.number = ""
        self.origname = ""
        self.prefix = ""
        self.suffix = ""

        self.origname = filename
        self.dirname = os.path.dirname(filename)
        self.basename = os.path.basename(filename)

        self.parse_folder_name()
        self.parse_filename()

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

    def tagstring(self):
        tagstring = ""
        if len(self.tags) > 0:
            tagstring = "#" + "#".join(sorted(set([tag.escape() for tag in self.tags])))

        return tagstring

    def current_path(self):
        filename = "%s-%s-%s%s.%s" % (
            self.date, self.event, self.number, self.tagstring(), self.suffix
        )

        return os.path.join(self.dirname, filename)

    def parse_filename(self):
        """
        Parses the filename to find the hashtags.
        """
        m = re.match(r"([^#]+)(#.*)*\.(\w+)", self.basename)

        self.tags = []

        if m is None:
            raise FilenameParseError('Could not parse "%s".' % self.basename)

        if not m.group(2) is None:
            taglist = m.group(2).split("#")

            for tag in taglist:
                if len(tag) > 0:
                    self.tags.append(Tag.from_escaped(tag))

        self.prefix = m.group(1)
        self.suffix = m.group(3)

        prefixparts = self.prefix.split('-')
        if len(prefixparts) < 3:
            raise PrefixParseError('Could not parse "%s".' % self.prefix)

        if self.date == "":
            self.date = prefixparts[0]
        if self.event == "":
            self.event = '-'.join(prefixparts[1:-1])

        self.number = prefixparts[-1]

    def parse_folder_name(self):
        """
        Parses date and event name from a folder name.
        """
        if len(self.dirname) == 0:
            return

        pattern = re.compile(r"([12]\d{3}[01]\d[0123]\d)-([^/]+)/?")
        album_dir = os.path.basename(self.dirname)
        m = pattern.match(album_dir)
        if m is None:
            raise FolderParseError('Could not parse "%s".' % album_dir)

        self.date = m.group(1)
        self.event = m.group(2)


class PictureParseError(Exception):
    pass

class FilenameParseError(PictureParseError):
    pass

class FolderParseError(PictureParseError):
    pass

class PrefixParseError(FilenameParseError):
    pass