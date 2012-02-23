#!/usr/bin/python
# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

from distutils.core import setup

setup(
    author = "Martin Ueding",
    author_email = "dev@martin-ueding.de",
    name = "picture_db_scripts",
    py_modules = [
        "hashtags",
    ],
    scripts = [
        "hash-tags",
        "picturerenamer",
    ],
    version = "1.1",
)
