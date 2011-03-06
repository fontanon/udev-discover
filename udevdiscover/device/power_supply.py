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
    parent = gudevice.get_parent()

    if parent:
        devtype = parent.get_driver()
        if devtype == 'ac':
            return ACAdapterDevice(gudevice)
        elif devtype == 'battery':
            return BatteryDevice(gudevice)

    return PowerSupplyDevice(gudevice)

class PowerSupplyDevice(Device):
    @property
    def nice_label(self):
        return _('Power supply device')
        
class ACAdapterDevice(Device):
    DEFAULT_ICON = 'ac-adapter'

    @property
    def nice_label(self):
        return _('A/C Adapter')

class BatteryDevice(Device):
    DEFAULT_ICON = 'battery'

    @property
    def nice_label(self):
        return _('Battery')
