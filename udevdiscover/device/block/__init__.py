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

__all__ = ['KB', 'MB', 'GB', 'BlockDevice', 'VolumeDevice', 'size_for_display']

import os

from udevdiscover.device import Device

KB = 1024.0
MB = KB * 1024.0
GB = MB * 1024.0

def size_for_display(size):
    if not size: return None

    if size < MB:
        return "%.1f KB" % (size / KB)
    elif size < GB:
        return "%.1f MB" % (size / MB)
    else:
        return "%.1f GB" % (size / GB)

def get_device_object(gudevice):
    devtype = gudevice.get_property('DEVTYPE')
    bus = gudevice.get_property('ID_BUS')

    if devtype == 'disk':
        if gudevice.get_property('ID_CDROM_MEDIA'):
            from optical import OpticalDiskDevice
            return OpticalDiskDevice(gudevice)
        elif gudevice.get_property('ID_CDROM'):
            from optical import OpticalDevice
            return OpticalDevice(gudevice)
        elif bus:
            from disk import DiskDevice
            return DiskDevice(gudevice)
        else:
            return BlockDevice(gudevice)
            
    elif devtype == 'partition':
        from partition import PartitionDevice
        return PartitionDevice(gudevice)

    else:
        return BlockDevice(gudevice)
        
class BlockDevice(Device):
    pass

class VolumeDevice(Device):
    BLOCK_SIZE = 512
    
    def __init__(self, gudevice):
        super(VolumeDevice, self).__init__(gudevice)

        self.size = None

        size_file = os.path.join(self.path, 'size')
        if os.path.exists(size_file):
            self.size = int(open(size_file).read()) * self.BLOCK_SIZE
