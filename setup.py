#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, platform
from distutils.core import setup
import glob

# Get current Python version
python_version = platform.python_version_tuple()

# Setup the default install prefix
prefix = sys.prefix

# Check our python is version 2.6 or higher
if python_version[0] >= 2 and python_version[1] >= 6:
    ## Set file location prefix accordingly
    prefix = '/usr/local'

# Get the install prefix if one is specified from the command line
for arg in sys.argv:
    if arg.startswith('--prefix='):
        prefix = arg[9:]
        prefix = os.path.expandvars(prefix)

# Gen .in files with @PREFIX@ replaced
for filename in ['udev-discover']:
    infile = open(filename + '.in', 'r')
    data = infile.read().replace('@PREFIX@', prefix)
    infile.close()

    outfile = open(filename, 'w')
    outfile.write(data)
    outfile.close()

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

        packages = ['udevdiscover', 'udevdiscover.device', 
            'udevdiscover.device.block', 'udevdiscover.device.input'], 
        package_dir =  {'udevdiscover': 'udevdiscover', 
            'udevdiscover.device': 'udevdiscover/device',
            'udevdiscover.device.block': 'udevdiscover/device/block',
            'udevdiscover.device.input': 'udevdiscover/device/input',
            },

        scripts = ['udev-discover'],
        
        data_files = [
            ('share/udev-discover', ['data/udev-discover.ui']),

            # You may need to call gtk-update-icon-cache -f -t $(datadir)/icons/hicolor
            # after installing icons
            ('share/icons/hicolor/16x16/devices', glob.glob('data/icons/16x16/devices/*')),
            ('share/icons/hicolor/22x22/devices', glob.glob('data/icons/22x22/devices/*')),
            ('share/icons/hicolor/24x24/devices', glob.glob('data/icons/24x24/devices/*')),
            ('share/icons/hicolor/48x48/devices', glob.glob('data/icons/48x48/devices/*')),
            ('share/icons/hicolor/scalable/devices', glob.glob('data/icons/scalable/devices/*')),
        ],
)
