.. Copyright © 2012-2013, 2017 Martin Ueding <dev@martin-ueding.de>

##################
picture-db-scripts
##################

Renames picture files according to a strict directory layout.

The ideal filename is::

    YYYYMMDD-Event/YYYYMMDD-Event-0000#Tag_1#Tag_2.jpg

Most files are in correctly named folders, the images lack proper names though.
This script parses the date and event name from the folder name and renames the
images. The image number is chosen from the last number found in the filename.
That way, some order is preserved and the file can be tracked through the
rename.

Use Cases
=========

Often, the images are named arbitrarily, like ``a.jpg``, not allowing them to
be tracked by their file name.

Other images are straight from the camera: ``IMG_3523.jpg``.

Then there are renames of the folder that change the implicit date for some
event, the images are not updated::

	20120225-Event/20120224-Event-001.jpg

The folder says one date, the picture says another date.

Tags In IPTC
============

The image tags belong into the IPTC fields, but not all program really obey
them. I came up with the hashtags in the filenames to make every dumb program
deal with the tags---by leaving them alone.

This script does a couple nice things:

#. Tags that are in the filename (hashtags) are “synced” to the IPTC fields.
#. Tags that are in the IPTC fields are “synced” to the filename.
#. Tags are sorted in the filename.
#. Tags are unique, double tags are eliminated in the process.

Dependencies
============

It uses the following external module:

- `iptcinfo <https://pypi.python.org/pypi/IPTCInfo>`_

Installation
============

To install it for yourself::

    ./setup.py install --user

A system wide install can be achieved using::

    make install

.. vim: spell
