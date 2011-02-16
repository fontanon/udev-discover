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

__all__ = ['OpticalDevice', 'OpticalDiskDevice']

from disk import DiskDevice
from udevdiscover.device.block import *

device_info_names = {
    'ID_CDROM_CD': 'CD-ROM',
    'ID_CDROM_CD_R': 'CD-R', 
    'ID_CDROM_CD_RW': 'CD-RW',
    'ID_CDROM_DVD': 'DVD-ROM',
    'ID_CDROM_DVD_R': 'DVD-R',
    'ID_CDROM_DVD_RW': 'DVD-RW',
    'ID_CDROM_DVD_RAM': 'DVD-RAM',
    'ID_CDROM_DVD_PLUS_R': 'DVD+R',
    'ID_CDROM_DVD_PLUS_RW': 'DVD+RW',
    'ID_CDROM_DVD_PLUS_R_DL': 'DVD+R DL',
    'ID_CDROM_DVD_PLUS_RW_DL': 'DVD+RW DL',
    'ID_CDROM_BD': 'Blu-ray',
    'ID_CDROM_BD_R': 'Blu-ray-R',
    'ID_CDROM_BD_RE': 'Blu-ray-RE',
    'ID_CDROM_HDDVD': 'HD DVD',
    'ID_CDROM_HDDVD_R': 'HD DVD-R',
    'ID_CDROM_HDDVD_RW': 'HD DVD-RW',
    'ID_CDROM_MO': 'CD-ROM Magneto optical',
    'ID_CDROM_MRW': 'CD-Mount Rainier RW',
    'ID_CDROM_MRW_W': 'CD-Mount Rainier RW-W',
}

# media info
media_info_names = {
    'ID_CDROM_MEDIA_CD': 'CD-ROM',
    'ID_CDROM_MEDIA_CD_R': 'CD-R', 
    'ID_CDROM_MEDIA_CD_RW': 'CD-RW',
    'ID_CDROM_MEDIA_DVD': 'DVD-ROM',
    'ID_CDROM_MEDIA_DVD_R': 'DVD-R',
    'ID_CDROM_MEDIA_DVD_RW': 'DVD-RW',
    'ID_CDROM_MEDIA_DVD_RAM': 'DVD-RAM',
    'ID_CDROM_MEDIA_DVD_PLUS_R': 'DVD+R',
    'ID_CDROM_MEDIA_DVD_PLUS_RW': 'DVD+RW',
    'ID_CDROM_MEDIA_DVD_PLUS_R_DL': 'DVD+R DL',
    'ID_CDROM_MEDIA_DVD_PLUS_RW_DL': 'DVD+RW DL',
    'ID_CDROM_MEDIA_BD': 'Blu-ray',
    'ID_CDROM_MEDIA_BD_R': 'Blu-ray-R',
    'ID_CDROM_MEDIA_BD_RE': 'Blu-ray-RE',
    'ID_CDROM_MEDIA_HDDVD': 'HD DVD',
    'ID_CDROM_MEDIA_HDDVD_R': 'HD DVD-R',
    'ID_CDROM_MEDIA_HDDVD_RW': 'HD DVD-RW',
    'ID_CDROM_MEDIA_MO': 'CD-ROM Magneto optical',
    'ID_CDROM_MEDIA_MRW': 'CD-Mount Rainier RW',
    'ID_CDROM_MEDIA_MRW_W': 'CD-Mount Rainier RW-W',

    'ID_CDROM_MEDIA_STATE': 'Media state',
    'ID_CDROM_MEDIA_SESSION_NEXT': 'Next Session',
    'ID_CDROM_MEDIA_SESSION_COUNT': 'Total Sessions',
    'ID_CDROM_MEDIA_SESSION_LAST_OFFSET': 'Session last offset',
    'ID_CDROM_MEDIA_TRACK_COUNT': 'Total tracks',
    'ID_CDROM_MEDIA_TRACK_COUNT_AUDIO': 'Audio tracks',
    'ID_CDROM_MEDIA_TRACK_COUNT_DATA': 'Data tracks',
}

class OpticalDevice(DiskDevice):
    DEFAULT_ICON = 'drive-optical'

    def get_summary(self):
        return (
            ('model', self.device.get_property('ID_MODEL') or 
                 self.device.get_property('ID_MODEL_ENC') or 'n/a'),
            ('vendor', self.device.get_property('ID_VENDOR') or 
                self.device.get_property('ID_VENDOR_ENC') or 'n/a'),
            ('device compatibility', '\n'.join(self.capabilities) or 'n/a'),
            ('firmware version', self.device.get_property('ID_REVISION') or 'n/a'),
            ('bus', self.bus or 'n/a'),
            ('device file', self.device.get_device_file() or 'n/a'),
        )

    @property
    def nice_label(self):
        return _('Optical Drive')

    @property
    def capabilities(self):
        return [v for k, v in device_info_names.items() \
            if self.get_props().has_key(k)]

    @property
    def label(self):
        return self.device.get_property('ID_FS_LABEL')


def find_mount_point(devfile):
    for row in file('/proc/mounts'):
        cols = row.split()
        if cols[0] == devfile:
            return cols[1]

    return None

class OpticalDiskDevice(OpticalDevice):
    DEFAULT_ICON = 'drive-optical'

    def get_summary(self):
        return (
            ('model', self.device.get_property('ID_MODEL') or 
                 self.device.get_property('ID_MODEL_ENC') or 'n/a'),
            ('vendor', self.device.get_property('ID_VENDOR') or 
                self.device.get_property('ID_VENDOR_ENC') or 'n/a'),
            ('media compatibility', '\n'.join(['%s: %s' % (k, v) for k, v in \
                self.capabilities]) or 'n/a'),
            ('firmware version', self.device.get_property('ID_REVISION') or 'n/a'),
            ('bus', self.bus or 'n/a'),
            ('device file', self.device.get_device_file() or 'n/a'),
            ('label', self.label or 'n/a'),
            ('mount point', find_mount_point(self.device.get_device_file()) or 'n/a'),
            ('format', self.device.get_property('ID_FS_TYPE') or 'n/a'),
            ('usage', self.device.get_property('ID_FS_USAGE') or 'n/a'),
        )

    @property
    def nice_label(self):
        return _('Optical Drive (media)')

    @property
    def capabilities(self):
        return [(v, self.device.get_property(k)) for k, v in media_info_names.items() \
            if self.get_props().has_key(k)]
