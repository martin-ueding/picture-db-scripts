#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

import logging
import re
import os.path
from iptcinfo import IPTCInfo

__docformat__ = "restructuredtext en"

next_id = 1
logging.basicConfig(level=logging.INFO)

class Tag(object):
    """
    Models a tag.
    """
    def __init__(self, text):
        """
        Creates a new Tag from human readable text.

        :param text: Human readable text.
        """
        self.text = text

    @staticmethod
    def from_escaped(escaped):
        """
        Creates a new Tag from escaped text.

        :param escaped: Escaped text.
        """
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

    def __hash__(self):
        return hash(self.text)


class Image(object):
    """
    Models an image filename with tags.
    """
    def __init__(self, filename):
        logging.info('Creating new Image from "%s".' % filename)
        self.basename = ""
        self.date = ""
        self.dirname = ""
        self.event = ""
        self.number = ""
        self.origname = ""
        self.prefix = ""
        self.suffix = ""
        self.iptc = None

        self.tags = set()

        self.origname = filename
        self.dirname = os.path.dirname(filename)
        self.basename = os.path.basename(filename)

        self._parse_folder_name()
        self._parse_filename()

        self._load_iptc()

    def add_tag(self, tag):
        """
        Adds the given tag.

        :param tag: Tag to add.
        :type tag: Tag
        :raise TypeError: Raised if not a hashtags.Tag given.
        """
        if not isinstance(tag, Tag):
            raise TypeError("Image::add_tag(hashtags.Tag)")

        self.tags.add(tag)

    def remove_tag(self, tag):
        """
        Removes the tag, if it is there.

        If the given tag is not in the set, no error is printed.

        :param tag: Tag to remove.
        :type tag: Tag
        """
        if not isinstance(tag, Tag):
            raise TypeError("Image::remove_tag(hashtags.Tag)")

        self.tags.discard(tag)

    def __repr__(self):
        return "Image('%s')" % self.current_path()

    def rename(self):
        newname = self.current_path()
        if os.path.isfile(newname):
            print 'File "%s" already exists.' % newname
            answer = raw_input('Do you want to increase the number? [Y/n] ')

            if answer != "n":
                while os.path.isfile(newname):
                    self.number = str(int(self.number) +1)
                    newname = self.current_path()

            print 'Now using "%s".' % newname

        assert not os.path.isfile(newname)

        logging.info('Renaming "%s" to "%s".' % (self.origname, newname))
        os.rename(self.origname, newname)

    def _tagstring(self):
        tagstring = ""
        if len(self.tags) > 0:
            tagstring = "#" + "#".join(sorted([tag.escape() for tag in self.tags]))

        return tagstring

    def current_path(self):
        filename = "%s-%s-%s%s.%s" % (
            self.date, self.event, self.number, self._tagstring(), self.suffix
        )

        return os.path.join(self.dirname, filename)

    def _parse_filename(self):
        """
        Parses the filename to find the hashtags.
        """
        m = re.match(r"([^#]+)(#.*)*\.(\w+)", self.basename)

        if m is None:
            raise FilenameParseError('Could not parse "%s".' % self.basename)

        if not m.group(2) is None:
            taglist = m.group(2).split("#")

            for tag in taglist:
                if len(tag) > 0:
                    self.add_tag(Tag.from_escaped(tag))

        self.prefix = m.group(1)
        self.suffix = m.group(3)

        self._parse_prefix()

    def _parse_prefix(self):
        prefixparts = self.prefix.split('-')

        if len(prefixparts) >= 3:
            if self.date == "":
                self.date = prefixparts[0]
            if self.event == "":
                self.event = '-'.join(prefixparts[1:-1])

            self.number = prefixparts[-1]

        # The number could not be parsed yet, try to find a number.
        if self.number == "":
            numbers = re.findall(r"\d+", self.prefix)
            if len(numbers) > 0:
                self.number = numbers[-1]

        if self.number == "":
            global next_id
            self.number = str(next_id)
            next_id += 1

        # In case anything is missing, this could not be parsed.
        if self.date == "":
            raise DateParseError('Could not parse "%s".' % self.prefix)
        if self.event == "":
            raise EventParseError('Could not parse "%s".' % self.prefix)
        if self.number == "":
            raise NumberParseError('Could not parse "%s".' % self.prefix)

    def _parse_folder_name(self):
        """
        Parses date and event name from a folder name.
        """
        if len(self.dirname) == 0:
            return

        pattern = re.compile(r"([012]\d{3}[01]\d[0123]\d)-([^/]+)/?")
        album_dir = os.path.basename(self.dirname)
        m = pattern.match(album_dir)
        if m is None:
            raise FolderParseError('Could not parse "%s".' % album_dir)

        self.date = m.group(1)
        self.event = m.group(2)

    def get_tags(self):
        return list(self.tags)

    def _load_iptc(self):
        try:
            self.iptc = IPTCInfo(self.origname, force=True)
        except IOError as e:
            pass
        else:
            logging.info('Found Tags "%s" in "%s".' % (', '.join(sorted(self.iptc.keywords)), self.origname))
            for keyword in self.iptc.keywords:
                self.add_tag(Tag(keyword))

    def write_iptc(self):
        self.iptc.data['keywords'] = list(sorted(self.get_tags()))
        logging.info('Saving IPTC keywords to "%s".' % self.origname)
        self.iptc.save()

    def name_changed(self):
        return self.origname != self.current_path()

    def iptc_changed(self):
       return sorted(map(Tag, self.iptc.keywords)) != sorted(self.get_tags())

    def save(self):
        if self.iptc_changed():
            self.write_iptc()

        if self.name_changed():
            self.rename()


class PictureParseError(Exception):
    pass

class FilenameParseError(PictureParseError):
    pass

class FolderParseError(PictureParseError):
    pass

class PrefixParseError(FilenameParseError):
    pass

class NumberParseError(PrefixParseError):
    pass

class EventParseError(PrefixParseError, FolderParseError):
    pass

class DateParseError(PrefixParseError, FolderParseError):
    pass
