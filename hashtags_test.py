#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

import unittest

from hashtags import *

class ParseFilenameTest(unittest.TestCase):
    def test_1(self):
        name, tags = parse_filename("20120204-Klopapierberg-9240#Martin_Ueding.jpg")
        self.assertEqual(name, '20120204-Klopapierberg-9240.jpg')
        self.assertEqual(tags, [Tag('Martin Ueding')])

    def test_2(self):
        name, tags = parse_filename("20120204-Klopapierberg-9240#Martin_Ueding#Another_Tag.jpg")
        self.assertEqual(name, '20120204-Klopapierberg-9240.jpg')
        self.assertEqual(tags, [Tag('Martin Ueding'), Tag('Another Tag')])


class GenerateFilenameTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(generate_filename('20120204-Klopapierberg-9240.jpg', [Tag('Martin_Ueding'), Tag('Another Tag')]), '20120204-Klopapierberg-9240#Another_Tag#Martin_Ueding.jpg')

    def test_2(self):
        self.assertEqual(generate_filename('20120204-Klopapierberg-9240.jpg', []), '20120204-Klopapierberg-9240.jpg')

    def test_3(self):
        self.assertEqual(generate_filename('20120204-Klopapierberg-9240.jpg', [Tag('Martin Ueding')]), '20120204-Klopapierberg-9240#Martin_Ueding.jpg')

    def test_4(self):
        name = generate_filename('20120204-Klopapierberg-9240.jpg', [Tag('Martin Ueding'), Tag('Martin Ueding')])
        self.assertEqual(name, '20120204-Klopapierberg-9240#Martin_Ueding.jpg')


class ImageTest(unittest.TestCase):
    def test_currentpath(self):
        image = Image("20120204-Klopapierberg-9240.jpg")
        image.add_tag(Tag("John Doe"))
        self.assertEqual(image.current_path(), "20120204-Klopapierberg-9240#John_Doe.jpg")

    def test_currentpath_empty(self):
        image = Image("a.jpg")
        image.add_tag(Tag("John Doe"))
        self.assertEqual(image.current_path(), "a#John_Doe.jpg")

    def test_add_tag_wrong_type(self):
        image = Image("a.jpg")
        with self.assertRaises(TypeError):
            image.add_tag("This is not a hashtag.Tag object")
