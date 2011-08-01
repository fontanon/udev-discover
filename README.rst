udev-discover:
==============

A tool for helping browsing the sysfs tree via udev focused on being helpfull 
for udev testers, coders, hackers and consumers.

Dependencies:
-------------

* python >= 2.5
* python-gconf
* python-gobject
* python-gudev
* python-gtk

Install udev-discover:
----------------------

Run as root::

    $ python setup.py install [--prefix=/this/is/optional]

You may also need to call, as root ...::

    $ gtk-update-icon-cache -f -t $(datadir)/icons/hicolor

... for the gtk icons cache being properly updated
where $(datadir) could be whether /usr/share or the prefix setted
on installing.
