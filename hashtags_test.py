#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

import unittest

from hashtags import *

class ParseFilenameTest(unittest.TestCase):
    def test_1(self):
        name, tags = parse_filename("20120204-Klopapierberg-9240#Martin_Ueding.jpg")
        assert name == '20120204-Klopapierberg-9240.jpg'
        assert tags == [Tag('Martin Ueding')]

    def test_2(self):
        name, tags = parse_filename("20120204-Klopapierberg-9240#Martin_Ueding#Another_Tag.jpg")
        assert name == '20120204-Klopapierberg-9240.jpg'
        assert tags == [Tag('Martin Ueding'), Tag('Another Tag')]


class GenerateFilenameTest(unittest.TestCase):
    def test_1(self):
        assert generate_filename('20120204-Klopapierberg-9240.jpg', [Tag('Martin_Ueding'), Tag('Another Tag')]) == '20120204-Klopapierberg-9240#Another_Tag#Martin_Ueding.jpg'

    def test_2(self):
        assert generate_filename('20120204-Klopapierberg-9240.jpg', []) == '20120204-Klopapierberg-9240.jpg'

    def test_3(self):
        assert generate_filename('20120204-Klopapierberg-9240.jpg', [Tag('Martin Ueding')]) == '20120204-Klopapierberg-9240#Martin_Ueding.jpg'
