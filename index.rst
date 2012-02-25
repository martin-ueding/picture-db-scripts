.. Picture DB Scripts documentation master file, created by
   sphinx-quickstart on Sat Feb 25 11:11:42 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Picture DB Scripts
==================


Renames picture files according to a strict directory layout.

The ideal filename is::

    YYYYMMDD-Event/YYYYMMDD-Event-0000#Tag_1#Tag_2.jpg

Most files are in correctly named folder, the images lack proper names though.
This script parses the date and event name from the folder name and renames the
images. The image number is chosen from any number found in the filename. That
way, some order is preserved and the file can be tracked through the rename.

Contents:
---------

.. toctree::
   :maxdepth: 2


   api/modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

