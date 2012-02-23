#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

import unittest

from picturedb import *

class ParseFilenameTest(unittest.TestCase):
    def test_without_folder(self):
        image = Image("20120204-Klopapierberg-9240#Martin_Ueding.jpg")
        self.assertEqual(image.date, '20120204')
        self.assertEqual(image.event, 'Klopapierberg')
        self.assertEqual(image.number, '9240')
        self.assertEqual(image.suffix, 'jpg')
        self.assertEqual(image.tags, [Tag('Martin Ueding')])

    def test_with_folder(self):
        image = Image("20120204-Klopapierberg/20120204-Klopapierberg-9240#Martin_Ueding.jpg")
        self.assertEqual(image.date, '20120204')
        self.assertEqual(image.event, 'Klopapierberg')
        self.assertEqual(image.number, '9240')
        self.assertEqual(image.suffix, 'jpg')
        self.assertEqual(image.tags, [Tag('Martin Ueding')])

    def test_with_different_folder(self):
        image = Image("20120204-Klopapierberg/00000000-Foobar2000-9240#Martin_Ueding.jpg")
        self.assertEqual(image.date, '20120204')
        self.assertEqual(image.event, 'Klopapierberg')
        self.assertEqual(image.number, '9240')
        self.assertEqual(image.suffix, 'jpg')
        self.assertEqual(image.tags, [Tag('Martin Ueding')])


class ParseWrongNames(unittest.TestCase):
    def test_single_number_with_folder(self):
        image = Image("20120204-Klopapierberg/1.jpg")
        self.assertEqual(image.date, '20120204')
        self.assertEqual(image.event, 'Klopapierberg')
        self.assertEqual(image.number, '1')
        self.assertEqual(image.suffix, 'jpg')

    def test_single_letter_with_folder(self):
        image = Image("20120204-Klopapierberg/a.jpg")
        self.assertEqual(image.date, '20120204')
        self.assertEqual(image.event, 'Klopapierberg')
        self.assertEqual(image.number, 'a')
        self.assertEqual(image.suffix, 'jpg')

    def test_single_number(self):
        with self.assertRaises(PrefixParseError):
            image = Image("1.jpg")
            self.assertEqual(image.number, '1')
            self.assertEqual(image.suffix, 'jpg')

    def test_single_letter(self):
        with self.assertRaises(PrefixParseError):
            image = Image("a.jpg")
            self.assertEqual(image.number, 'a')
            self.assertEqual(image.suffix, 'jpg')


class GenerateFilenameTest(unittest.TestCase):
    def test_tags(self):
        """
        Tests whether tags are working.

            - Double tags have to be ignored.
            - Tags have to be sorted.
        """
        image = Image('20120204-Klopapierberg-9240.jpg')
        image.add_tag(Tag('Martin_Ueding'))
        image.add_tag(Tag('Another Tag'))
        image.add_tag(Tag('Another Tag'))
        self.assertEqual(image.current_path(), '20120204-Klopapierberg-9240#Another_Tag#Martin_Ueding.jpg')

    def test_without_folder(self):
        image = Image('20120204-Klopapierberg-9240.jpg')
        self.assertEqual(image.current_path(), '20120204-Klopapierberg-9240.jpg')

    def test_with_folder(self):
        image = Image('20120204-Klopapierberg/00000000-Foo-9240.jpg')
        self.assertEqual(image.current_path(), '20120204-Klopapierberg/20120204-Klopapierberg-9240.jpg')


class AddTagTest(unittest.TestCase):
    def test_currentpath(self):
        image = Image("20120204-Klopapierberg-9240.jpg")
        image.add_tag(Tag("John Doe"))
        self.assertEqual(image.current_path(), "20120204-Klopapierberg-9240#John_Doe.jpg")

    def test_add_tag_wrong_type(self):
        image = Image("00000000-A-1.jpg")
        with self.assertRaises(TypeError):
            image.add_tag("This is not a hashtag.Tag object")
