# -*- coding: utf-8 -*-
# vim: ts=4 
###
#
# Copyright (c) 2010 J. Félix Ontañón
#
# Almost based on arista.inputs module:
# Copyright 2008 - 2010 Daniel G. Taylor <dan@programmer-art.org>
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

import gudev

def get_device_object(device):
    subsys = device.get_subsystem()

    if subsys == 'usb':
        import usb
        return usb.get_device_object(device)
    elif subsys == 'pci':
        import pci 
        return pci.get_device_object(device)
    elif subsys == 'block':
        import block
        return block.get_device_object(device)
    elif subsys == 'scsi':
        import scsi
        return scsi.get_device_object(device)
    elif subsys == 'input':
        import input
        return input.get_device_object(device)
    elif subsys == 'net':
        import net
        return net.get_device_object(device)
    elif subsys == 'power_supply':
        import power_supply
        return power_supply.get_device_object(device)
    else:
        return Device(device)

class Device(object):
    '''A simple object representing a device.'''

    DEFAULT_ICON = 'gtk-dialog-question'
    UNKNOWN_DEV = 'Unknown Device'
    DEVICE_TYPE_STR = {gudev.DEVICE_TYPE_BLOCK: 'block', 
        gudev.DEVICE_TYPE_CHAR: 'char',
        gudev.DEVICE_TYPE_NONE: 'n/a'
    }

    def __init__(self, device):
        '''Create a new input device
            
        @type device: gudev.Device
        @param device: The device we are using
        '''
        self.device = device

    @property
    def nice_label(self):
        return self.device.get_name() or self.UNKNOWN_DEV

    @property
    def icon(self):
        return self.DEFAULT_ICON

    @property
    def parent(self):
        parent_device = self.device.get_parent()
        if parent_device:
            return Device(parent_device)
        else:
            return None

    def get_info(self):
        return (
            ('subsystem', self.device.get_subsystem() or 'n/a'),
            ('devtype', self.device.get_devtype() or 'n/a'),
            ('name', self.device.get_name() or 'n/a'),
            ('number', self.device.get_number() or 'n/a'),
            ('sysfs_path', self.device.get_sysfs_path() or 'n/a'),
            ('driver', self.device.get_driver() or 'n/a'),
            ('action', self.device.get_action() or 'n/a'),
            ('seqnum', self.device.get_seqnum() or 'n/a'),
            ('device type', self.DEVICE_TYPE_STR[self.device.get_device_type()]),
            ('device number', str(self.device.get_device_number()) or 'n/a'),
            ('device file', self.device.get_device_file() or 'n/a'),
            ('device file symlinks', 
                '\n'.join(self.device.get_device_file_symlinks()) or 'n/a')
        )

    def get_props(self):
        props = {}
        for device_key in self.device.get_property_keys():
            props[device_key] = self.device.get_property(device_key)

        return props
    
    @property
    def path(self):
        '''Get the sysfs_path for this device
            
        @rtype: string
        @return: The sysfs path
        '''
        return self.device.get_sysfs_path()

    @property
    def subsystem(self):
        return self.device.get_subsystem()

    def __repr__(self):
        return self.nice_label

    def __eq__(self, dev):
        if dev == None:
            return False
        else:
            return self.path == dev.path
