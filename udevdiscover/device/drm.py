# -*- coding: utf-8 -*-
# vim: ts=4 
###
#
# Copyright (c) 2011 J. Félix Ontañón
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
    return DRMDevice(gudevice)

class DRMDevice(Device):
    DEFAULT_ICON = 'video-display'

    @property
    def nice_label(self):
        return _('Direct Rendering Manager Device')
