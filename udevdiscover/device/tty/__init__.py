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

from udevdiscover.device import Device

def get_device_object(gudevice):
    return SerialDevice(gudevice)

class SerialDevice(Device):
    def __init__(self, gudevice):
        super(SerialDevice, self).__init__(gudevice)

        devname = gudevice.get_name()
        devpath = gudevice.get_sysfs_path()

        if devname.startswith('ttyS'):
            self.__type = 'platform'
        elif devname.startswith('ttyUSB'):
            self.__type = 'usb'
        elif devname.startswith('ttyACM'):
            self.__type = 'modem'
        elif self.path.startswith('/sys/devices/virtual'):
            self.__type = 'virtual'
        else:
            self.__type = None

    @property
    def nice_label(self):
        if self.type == 'platform':
            return _('%s Serial Port') % self.parent.nice_label
        elif self.type == 'usb':
            return _('USB Serial Port')
        elif self.type == 'modem':
            return _('Modem Serial Port')
        elif self.type == 'virtual':
            return _('Virtual Serial Port')
        else:
            return _('Serial Port')

    @property
    def icon(self):
        if self.type == 'modem':
            return 'modem'
        else:
            return self.DEFAULT_ICON

    @property
    def type(self):
        return self.__type
