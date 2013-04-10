#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

from distutils.core import setup

setup(
    author = "Martin Ueding",
    author_email = "dev@martin-ueding.de",
    name = "picture_db_scripts",
    py_modules = [
        "picturedb",
    ],
    scripts = [
        "hashtag",
    ],
    version = "2.1.2",
)
