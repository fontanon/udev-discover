# -*- coding: utf-8 -*-
# vim: ts=4 
###
#
# Copyright (c) 2010 J. Félix Ontañón
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

__all__ = ['PartitionDevice']

import os

from udevdiscover.device.block import *

def find_mount_point(devfile):
    for row in file('/proc/mounts'):
        cols = row.split()
        if cols[0] == devfile:
            return cols[1]

    return None

def volume_stats(devfile):
    mount_point = find_mount_point(devfile)
    if mount_point and os.path.ismount(mount_point):
        return os.statvfs(mount_point)

class PartitionDevice(VolumeDevice):
    DEFAULT_ICON = 'drive-harddisk'

    def get_summary(self):
        return (
            ('usage', self.device.get_property('ID_FS_USAGE') or 'n/a'),
            ('format', self.device.get_property('ID_FS_TYPE') or 'n/a'),
            ('device file', self.device.get_device_file() or 'n/a'),
            ('mount point', find_mount_point(self.device.get_device_file()) or 'n/a'),
            ('label', self.device.get_property('ID_FS_LABEL') or 'n/a'),
            ('size', size_for_display(self.size) or 'n/a'),
            ('free', self.volume_free and size_for_display(self.volume_free) or 'n/a'),
        )

    @property
    def nice_label(self):
        if self.size:
            return _('%s Volume') % size_for_display(self.size)

        return _('Partition')

    @property
    def volume_free(self):
        for devfile in [self.device.get_device_file()] + \
                self.device.get_device_file_symlinks():
            stats = volume_stats(devfile)
            if stats: return stats.f_bsize * stats.f_bfree

        return None
