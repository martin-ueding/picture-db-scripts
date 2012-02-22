#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

import re

def parse_filename(name):
    """
    Parses the filename to find the hashtags.

    >>> parse_filename("20120204-Klopapierberg-9240#Martin_Ueding.jpg")
    ('20120204-Klopapierberg-9240.jpg', ['Martin_Ueding'])

    >>> parse_filename("20120204-Klopapierberg-9240#Martin_Ueding#Another_Tag.jpg")
    ('20120204-Klopapierberg-9240.jpg', ['Martin_Ueding', 'Another_Tag'])

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
                result.append(tag)

        filename = m.group(1)+m.group(3)

    return filename, result


def generate_filename(filename, tags):
    """
    >>> generate_filename('20120204-Klopapierberg-9240.jpg', ['Martin_Ueding', 'Another_Tag'])
    '20120204-Klopapierberg-9240#Another_Tag#Martin_Ueding.jpg'

    >>> generate_filename('20120204-Klopapierberg-9240.jpg', [])
    '20120204-Klopapierberg-9240.jpg'

    >>> generate_filename('20120204-Klopapierberg-9240.jpg', ['Martin_Ueding'])
    '20120204-Klopapierberg-9240#Martin_Ueding.jpg'
    """
    m = re.match(r"([^.]+)(\.\w+)", filename)

    if not m is None:
        name = m.group(1)
        suffix = m.group(2)

        if len(tags) == 0:
            taglist = ""
        else:
            taglist = "#"+"#".join(sorted(tags))

        return name+taglist+suffix
