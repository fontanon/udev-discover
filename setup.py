#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, platform
import glob
import subprocess

from distutils.core import setup
from distutils.command.build import build
from distutils.command.build_scripts import build_scripts
from distutils.command.install_data import install_data
from distutils.log import warn, info, error, fatal
from distutils.dep_util import newer

PO_DIR = 'po'
MO_DIR = os.path.join('build', 'mo')

def replace_prefix(prefix):
    # Gen .in files with @PREFIX@ replaced
    for filename in ['udev-discover']:
        infile = open(filename + '.in', 'r')
        data = infile.read().replace('@PREFIX@', prefix)
        infile.close()

        outfile = open(filename, 'w')
        outfile.write(data)
        outfile.close()

def compile_po():
    for po in glob.glob (os.path.join (PO_DIR, '*.po')):
        lang = os.path.basename(po[:-3])
        mo = os.path.join(MO_DIR, lang, 'udevdiscover.mo')

        directory = os.path.dirname(mo)
        if not os.path.exists(directory):
            info('creating %s' % directory)
            os.makedirs(directory)

        if newer(po, mo):
            info('compiling %s -> %s' % (po, mo))
            try:
                rc = subprocess.call(['msgfmt', '-o', mo, po])
                if rc != 0:
                    raise Warning, "msgfmt returned %d" % rc
            except Exception, e:
                error("Building gettext files failed.  Try setup.py \
                    --without-gettext [build|install]")
                error("Error: %s" % str(e))
                sys.exit(1)

class BuildData(build):
    user_options = build.user_options
    user_options.extend([('prefix=', None, "installation prefix")])

    def initialize_options(self):
        build.initialize_options(self)
        self.prefix = None

    def finalize_options(self):
        build.finalize_options(self)
        if not self.prefix:
            install = self.distribution.get_command_obj('install', False)
            if install:
                self.prefix = install.prefix
            else:
                self.prefix = sys.prefix

    def run (self):
        replace_prefix(self.prefix)
        build.run (self)
        compile_po()

class BuildScript(build_scripts):
    user_options = build_scripts.user_options
    user_options.extend([('prefix=', None, "installation prefix")])

    def initialize_options(self):
        build_scripts.initialize_options(self)
        self.prefix = None

    def finalize_options(self):
        build_scripts.finalize_options(self)
        if not self.prefix:
            install = self.distribution.get_command_obj('install', False)
            if install:
                self.prefix = install.prefix
            else:
                self.prefix = sys.prefix

    def run(self):
        replace_prefix(self.prefix)
        build_scripts.run (self)
        compile_po()

class InstallData(install_data):
    def run (self):
        self.data_files.extend (self._find_mo_files ())
        install_data.run (self)

    def _find_mo_files (self):
        data_files = []

        for mo in glob.glob (os.path.join (MO_DIR, '*', 'udevdiscover.mo')):
            lang = os.path.basename(os.path.dirname(mo))
            dest = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
            data_files.append((dest, [mo]))

        return data_files

setup(
        name='udev-discover',
        version='0.2.1',
        description='A GUI tool for exploring the present devices on the system',
        author='J. Félix Ontañón',
        author_email='fontanon@emergya.es',
        url='http://gitorious.org/udev-discover/udev-discover',

        classifiers=[
            'Development Status :: 0.2.1 - Beta',
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

        cmdclass={'build':BuildData, 'build_scripts':BuildScript, 'install_data':InstallData},

        data_files = [
            ('share/udev-discover', ['data/udev-discover.ui']),
            ('share/udev-discover', ['data/udev-discover.svg']),
            ('share/pixmaps', ['data/udev-discover.svg']),
            ('/etc/gconf/schemas', ['data/udev-discover.schemas']),
            ('share/applications', ['data/udev-discover.desktop']),

            # You may need to call gtk-update-icon-cache -f -t $(datadir)/icons/hicolor
            # after installing icons
            ('share/icons/hicolor/16x16/devices', glob.glob('data/icons/16x16/devices/*')),
            ('share/icons/hicolor/22x22/devices', glob.glob('data/icons/22x22/devices/*')),
            ('share/icons/hicolor/24x24/devices', glob.glob('data/icons/24x24/devices/*')),
            ('share/icons/hicolor/48x48/devices', glob.glob('data/icons/48x48/devices/*')),
            ('share/icons/hicolor/scalable/devices', glob.glob('data/icons/scalable/devices/*')),
            ('share/icons/hicolor/scalable/apps', ['data/udev-discover.svg']),
        ],
)
