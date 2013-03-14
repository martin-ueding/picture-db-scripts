#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

"""
Library that encapsulates most of the logic in the picture database. There are
classes to model images and tags on those images. Additionally, there are
methods that can act on colletions of images.
"""

from iptcinfo import IPTCInfo
import itertools
import logging
import os.path
import re
import uuid

__docformat__ = "restructuredtext en"

next_id = 1
logging.basicConfig(level=logging.FATAL)

class Tag(object):
    """
    Models a tag.

    To make the tag filename safe, it does the following:

    - Space with ``_``
    """

    replacements = [
        (' ', '_'),
    ]
    """
    List with replacements to make them filename safe.
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
        :return: Unescaped text.
        """
        unescaped = re.sub(r"_", " ", escaped)
        for replace, pattern in Tag.replacements:
            unescaped = re.sub(pattern, replace, unescaped)
        return Tag(unescaped)

    def escape(self):
        """
        Makes the given tag name file name safe.

        :return: Escaped string.
        """
        escaped = self.text
        for pattern, replace in self.replacements:
            escaped = re.sub(pattern, replace, escaped)
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
        :raise TypeError: Raised if not a :py:class:`Tag` given.
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
        """
        Performs the actual renaming.

        If the file exists, it will try to increase the picture number. If the
        attribute :py:attr:`tempname` is set, this name will be used instead of
        :py:attr:`origname`.
        """
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

        oldname = self.origname
        try:
            oldname = self.tempname
        except AttributeError:
            pass

        logging.info('Renaming "%s" to "%s".' % (self.origname, newname))
        os.rename(oldname, newname)

    def _tagstring(self):
        tagstring = ""
        if len(self.tags) > 0:
            tagstring = "#" + "#".join(sorted([tag.escape() for tag in self.tags]))

        return tagstring

    def current_path(self):
        """
        Gives the current path of this image.
        
        :return: Current path.
        :rtype: str
        """
        filename = "%s-%s-%s%s.%s" % (
            self.date, self.event, self.number, self._tagstring(), self.suffix
        )

        return os.path.join(self.dirname, filename)

    def _parse_filename(self):
        """
        Parses the filename to find the hashtags.

        :raises FilenameParseError: Raised if name could not be parsed.
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
        """
        Parses the first part of the filename.

        If date or event are already set from the folder name, they are not
        overwritten.
        """
        prefixparts = self.prefix.split('-')

        if len(prefixparts) >= 3:
            if self.date == "":
                self.date = prefixparts[0]
            if self.event == "":
                self.event = '-'.join(prefixparts[1:-1])

            self.number = prefixparts[-1]

        # The number could not be parsed yet, try to find a number. At this
        # point, any number is fine.
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

        Sets :py:attr:`date` and :py:attr:`event`.
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
        """
        Gives the list with all tags.

        :return: A list with all tags.
        :rtype: list
        """
        return list(self.tags)

    def _load_iptc(self):
        """
        Loads the IPTC data from the original file and saves them with
        :py:meth:`add_tag`.
        """
        try:
            self.iptc = IPTCInfo(self.origname, force=True)
        except IOError as e:
            pass
        else:
            logging.info('Found Tags "%s" in "%s".' % (', '.join(sorted(self.iptc.keywords)), self.origname))
            for keyword in self.iptc.keywords:
                self.add_tag(Tag(keyword))

    def write_iptc(self):
        """
        Writes the IPTC data.
        """
        self.iptc.data['keywords'] = list(sorted(self.get_tags()))
        logging.info('Saving IPTC keywords to "%s".' % self.origname)
        self.iptc.save()

    def name_changed(self):
        """
        Checks whether the name that :py:meth:`current_path` gives is the same
        than :py:attr:`origname`.

        :return: Whether the filename was changed.
        :rtype: bool
        """
        return self.origname != self.current_path()

    def iptc_changed(self):
        """
        Check whether the tags match the IPTC tags.

        :return: Whether the IPTC tags need to be rewritten.
        :rtype: bool
        """
        return sorted(map(Tag, self.iptc.keywords)) != sorted(self.get_tags())

    def save(self):
        """
        Renames the file and updates the IPTC fields.
        """
        if self.iptc_changed():
            self.write_iptc()

        if self.name_changed():
            self.rename()

    def rename_to_temp(self):
        """
        Renames the image to a temporary name.

        It generates a random UUID 4 and renames the picture to it. The
        temporary name is stored in the :py:attr:`tempname` attribute.
        """
        self.tempname = str(uuid.uuid4())
        os.rename(self.origname, self.tempname)

class PictureParseError(Exception):
    """
    General exception class for parsing the information in the file names.
    """
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
    """
    Error related to the parsing of the event from either folder or image.
    """
    pass

class DateParseError(PrefixParseError, FolderParseError):
    """
    Error related to the parsing the date from either the folder or the image
    file.
    """
    pass

def compress_numbers(images):
    """
    Compresses the numbers in the filenames.

    This has to be done to a whole collection so that they are numbered
    correctly. The number of images are taken into account when padding the
    number with leadings zeros.

    :param images: Images to rename.
    :type images: list
    """
    image_count = len(images)
    digit_count = len(str(image_count))
    format_string = '{:0'+str(digit_count)+'d}'

    for n, image in zip(itertools.count(1), images):
        image.number = format_string.format(n)

def batch_rename(images):
    """
    Renames a whole batch of images, avoiding temporary name collisions.

    Say you have images like so:

    - foo-0.jpg
    - foo-1.jpg
    - foo-2.jpg

    If you use the compress option, the images will be renamed to:

    - foo-1.jpg
    - foo-2.jpg
    - foo-3.jpg

    The problem is that those names are always in use, so that renaming will
    fail. This function renames all images to some temporary name and then
    renames them all back.
    """
    for image in images:
        image.rename_to_temp()

    for image in images:
        image.rename()
