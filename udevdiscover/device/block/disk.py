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

__all__ = ['DiskDevice']

import os

from udevdiscover.device.block import *

class DiskDevice(VolumeDevice):
    DEFAULT_ICON = 'drive-harddisk'
    
    def get_summary(self):
        return (
            ('model', self.device.get_property('ID_MODEL') or 
                 self.device.get_property('ID_MODEL_ENC') or 'n/a'),
            ('vendor', self.device.get_property('ID_VENDOR') or 
                self.device.get_property('ID_VENDOR_ENC') or 'n/a'),
            ('device file', self.device.get_device_file() or 'n/a'),
            ('serial number', self.device.get_property('ID_SERIAL_SHORT') or 
                self.device.get_property('ID_SERIAL') or 'n/a'),
            ('firmware version', self.device.get_property('ID_REVISION') or 'n/a'),
            ('bus', self.bus or 'n/a'),
            ('type', self.device.get_property('ID_TYPE') or 'n/a'),
        )

    @property
    def nice_label(self):
        if self.size:
            return _('%s Mass Storage Drive') % size_for_display(self.size)
        else:
            return _('Mass Storage Drive')
    
    @property
    def bus(self):
        return self.device.get_property('ID_BUS')

    @property
    def vendor_name(self):
        return self.device.get_property('ID_VENDOR')

    @property
    def model_name(self):
        return self.device.get_property('ID_MODEL')
