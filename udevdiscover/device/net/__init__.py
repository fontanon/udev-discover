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

import os
from udevdiscover.device import Device

KB = 1024.0
MB = KB * 1024.0
GB = MB * 1024.0

def size_for_display(size):
    if not size: return None

    size = int(size)

    if size < MB:
        return "%.1f KB" % (size / KB)
    elif size < GB:
        return "%.1f MB" % (size / MB)
    else:
        return "%.1f GB" % (size / GB)

def get_device_object(device):
    return NetDevice(device)

class NetDevice(Device):
    DEFAULT_ICON = 'network-wired'

    def get_summary(self):
        def read_sysfs_file(filepath):
            if os.path.exists(filepath):
                f = open(filepath, 'r')
                cont = f.read()
                f.close()
                if cont[-1] == '\n': cont = cont[:-1]
                return cont
            return None

        return (
            ('interface', self.device.get_property('INTERFACE') or 'n/a'),
            ('mac address', read_sysfs_file(os.path.join(self.path, 
                'address')) or 'n/a'),
            ('operation state', read_sysfs_file(os.path.join(self.path, 
                'operstate')) or 'n/a'),
            ('rx bytes', size_for_display(read_sysfs_file(os.path.join(self.path, 
                'statistics/rx_bytes'))) or 'n/a'),
            ('tx bytes', size_for_display(read_sysfs_file(os.path.join(self.path, 
                'statistics/tx_bytes'))) or 'n/a'),
        )

    @property
    def nice_label(self):
        if self.device.get_devtype() == 'wlan':
            return _('Wireless Network Device')
        else:
            return _('Network Device')

    @property
    def icon(self):
        if self.device.get_devtype() == 'wlan':
            return 'network-wireless'
        else:
            return self.DEFAULT_ICON

    @property
    def vendor_name(self):
        return self.device.get_property('ID_VENDOR_FROM_DATABASE')

    @property
    def model_name(self):
        return self.device.get_property('ID_MODEL_FROM_DATABASE')
