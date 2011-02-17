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

def get_device_object(device):
    if device.get_name().startswith('input'):
        return InputDevice(device)

    property_keys = device.get_property_keys()

    if 'ID_INPUT_KEYBOARD' in property_keys:
        from keyboard import KeyboardDevice
        return KeyboardDevice(device)
    elif 'ID_INPUT_MOUSE' in property_keys:
        from mouse import MouseDevice
        return MouseDevice(device)
    elif 'ID_INPUT_TOUCHPAD' in property_keys:
        from touchpad import TouchpadDevice
        return TouchpadDevice(device)
    elif 'ID_INPUT_JOYSTICK' in property_keys:
        from joystick import JoystickDevice
        return JoystickDevice(device)
    elif 'ID_INPUT_TOUCHSCREEN' in property_keys:
        from touchscreen import TouchscreenDevice
        return TouchscreenDevice(device)
    elif 'ID_INPUT_TABLET' in property_keys:
        from tablet import TabletDevice
        return TabletDevice(device)
    elif device.get_name().startswith('event'):
        return EventDevice(device)
    else:
        return InputDevice(device)

class InputDevice(Device):
    @property
    def nice_label(self):
        return _('Input Device')

    @property
    def vendor_name(self):
        name = self.device.get_property('NAME')
        if name:
            return name.replace('"','')
        else:
            return None

class EventDevice(Device):
    @property
    def nice_label(self):
        return _('Event Device')
