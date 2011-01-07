# -*- coding: utf-8 -*-
# vim: ts=4 
###
#
# Copyright (c) 2010 J. Félix Ontañón
#
# pci_class_names adapted from gnome-device-manager
# Copyright (C) 2007 David Zeuthen
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors : J. Félix Ontañón <fontanon@emergya.es>
# 

import os

from udevdiscover.device import Device

KB = 1024.0
MB = KB * 1024.0
GB = MB * 1024.0

def get_device_object(device):
    return BlockDevice(device)

def size_for_display(size):
    if size < MB:
        return "%.1f KB" % (size / KB)
    elif size < GB:
        return "%.1f MB" % (size / MB)
    else:
        return "%.1f GB" % (size / GB)

def volume_stats(devfile):
    def find_mount_point(devfile):
        for row in file('/proc/mounts'):
            cols = row.split()
            if cols[0] == devfile:
                return cols[1]

        return None

    mount_point = find_mount_point(devfile)
    if mount_point and os.path.ismount(mount_point):
        return os.statvfs(mount_point)

class BlockDevice(Device):
    def get_info(self):
        return {
            'model': self.device.get_property('ID_MODEL') or 
                 self.device.get_property('ID_MODEL_ENC') or 'n/a',
            'vendor': self.device.get_property('ID_VENDOR') or 
                self.device.get_property('ID_VENDOR_ENC') or 'n/a',
            'device file': self.device.get_device_file() or 'n/a',
            'serial number': self.device.get_property('ID_SERIAL_SHORT') or 
                self.device.get_property('ID_SERIAL') or 'n/a',
            'firmware version': self.device.get_property('ID_REVISION') or 'n/a',
            'bus': self.device.get_property('ID_BUS') or 'n/a',
            'type': self.device.get_property('ID_TYPE') or 'n/a',
            'size': self.volume_size and size_for_display(self.volume_size) or 'n/a',
            'free': self.volume_free and size_for_display(self.volume_free) or 'n/a',
        }

    @property
    def nice_label(self):
        return _('Mass Storage Device')

    @property
    def volume_size(self):
        for devfile in [self.device.get_device_file()] + \
                self.device.get_device_file_symlinks():
            stats = volume_stats(devfile)
            if stats: return stats.f_bsize * stats.f_blocks

        return None

    @property
    def volume_free(self):
        for devfile in [self.device.get_device_file()] + \
                self.device.get_device_file_symlinks():
            stats = volume_stats(devfile)
            if stats: return stats.f_bsize * stats.f_bfree

        return None
