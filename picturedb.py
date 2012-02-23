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
        self.origname = filename
        self.dirname = os.path.dirname(filename)
        self.basename = os.path.basename(filename)
        self.filename, self.tags = self.parse_filename()

    def add_tag(self, tag):
        """
        @type tag: Tag
        @raise TypeError: Raised if not a hashtags.Tag given.
        """
        if not isinstance(tag, Tag):
            raise TypeError("Image::add_tag(hashtags.Tag)")

        self.tags.append(tag)

    def current_path(self):
        newname = generate_filename(self.filename, self.tags)
        return os.path.join(self.dirname, newname)

    def __repr__(self):
        return "Image(%s)" % self.current_path()

    def rename(self):
        os.rename(self.origname, self.current_path())

    def parse_filename(self):
        """
        Parses the filename to find the hashtags.

        @return: Filename, list with tags.
        @rtype: tuple
        """
        m = re.match(r"([^#]+)(#.*)+(\.\w+)", self.basename)

        result = []
        filename = name

        if not m is None:
            taglist = m.group(2).split("#")

            for tag in taglist:
                if len(tag) > 0:
                    result.append(Tag.from_escaped(tag))

            filename = m.group(1) + m.group(3)

        return filename, result

    def generate_filename(self):
        m = re.match(r"([^.]+)(\.\w+)", self.filename)

        if not m is None:
            name = m.group(1)
            suffix = m.group(2)

            if len(tags) == 0:
                taglist = ""
            else:
                escaped = [tag.escape() for tag in self.tags]
                tagset = sorted(set(escaped))
                taglist = "#"+"#".join(tagset)

            return name+taglist+suffix

    def parse_folder_name(name):
        """
        Parses date and event name from a folder name.

        If the folder does not match, return C{None}.

        @param name: Folder name
        @type name: str
        @return: Date, event name.
        @rtype: tuple
        """
        pattern = re.compile(r"([12]\d{3}[01]\d[0123]\d)-([^/]+)/?")
        m = pattern.match(name)
        if m is not None:
            return m.group(1), m.group(2)

        return None


    def parse_file_name(name):
        """
        Parses date, eventname and number from a image file.

        If the image file name does not match, return C{None}.

        @param name: Folder name
        @type name: str
        @return: Date, eventname, number.
        @rtype: tuple
        """
        pattern = re.compile(r"([12]\d{3}[01]\d[0123]\d)-([^-]+)-(\d+).*\..*")
        m = pattern.match(name)
        if m is not None:
            return m.group(1), m.group(2), m.group(3)

        return None


    def find_number(name):
        """
        Tries to find a number in the image file.

        @param name: Image file name.
        @type name: str
        @return: Number, suffix.
        @rtype: tuple
        """
        pattern = re.compile(r"\D*(\d+)\D*[^.]*\.(.*)")
        m = pattern.match(name)
        if m is not None:
            return m.group(1), m.group(2)

        return None


    def new_name(folder, date, name, number, tags, suffix):
        """
        Generates a new name from given data.

        @param folder: Folder the files goes into.
        @type folder: str
        @param date: Date string.
        @type date: str
        @param name: Event name.
        @type name: str
        @param number: Image number.
        @type number: str
        @param suffix: File suffix.
        @type suffix: str
        @return: Generated filename.
        @rtype: str
        """
        n = "%s/%s-%s-%s%s.%s" % (folder, date, name, number, tags, suffix)
        n = n.replace(r"//", r"/")
        return n

    def find_tags(filename):
        pattern = re.compile(r"[^#]*(#[^.]+)\..*")
        m = pattern.match(filename)
        if m is not None:
            return m.group(1)
        else:
            return ""


