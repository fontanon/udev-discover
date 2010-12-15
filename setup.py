#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
        name='udev-discover',
        version='0.1',
        description='A GUI tool for exploring the present devices on the system',
        author='J. Félix Ontañón',
        author_email='fontanon@emergya.es',
        url='http://gitorious.org/udev-discover/udev-discover',

        classifiers=[
            'Development Status :: 0.1 - Alpha',
            'Environment :: Desktop Environment',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: POSIX',
            'Programming Language :: Python',
	        'Topic :: Utilities'
        ],
        
        keywords = ['python', 'udev', 'gnome'],

        packages = ['udevdiscover'],
        package_dir =  {'udevdiscover': 'udevdiscover'},

        scripts = ['udev-discover'],
        
        data_files = [
            ('/usr/local/share/udev-discover', ['udev-discover.ui']),
        ]
)
