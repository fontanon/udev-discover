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

class TabletDevice(Device):
    DEFAULT_ICON = 'input-tablet'

    @property
    def nice_label(self):
        if self.device.get_name().startswith('ev'):
             return _('Tablet Event')
        else:
            return _('Tablet Device')

    @property
    def vendor_name(self):
        return self.device.get_property('ID_VENDOR')

    @property
    def model_name(self):
        return self.device.get_property('ID_MODEL')
