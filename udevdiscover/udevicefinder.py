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

import gobject
import gudev
from usb import get_usb_short_long_names
from pci import get_pci_short_long_names

UNKNOWN_DEV = 'Unknown Device'
DEVICE_TYPE_STR = {gudev.DEVICE_TYPE_BLOCK: 'block', 
    gudev.DEVICE_TYPE_CHAR: 'char',
    gudev.DEVICE_TYPE_NONE: 'n/a'
}

class Device(object):
    '''A simple object representing a device.'''
    
    def __init__(self, device):
        '''Create a new input device
            
        @type device: gudev.Device
        @param device: The device we are using
        '''
        self.device = device

    @property
    def nice_label(self):
        return self.device.get_name() or UNKNOWN_DEV

    @property
    def parent(self):
        parent_device = self.device.get_parent()
        if parent_device:
            return Device(parent_device)
        else:
            return None

    def get_info(self):
        return {'subsystem': self.device.get_subsystem() or 'n/a',
            'sysfs_path': self.device.get_sysfs_path() or 'n/a',
            'devtype': self.device.get_devtype() or 'n/a',
            'driver': self.device.get_driver() or 'n/a',
            'action': self.device.get_action() or 'n/a',
            'seqnum': self.device.get_seqnum() or 'n/a',
            'device type': DEVICE_TYPE_STR[self.device.get_device_type()],
            'device number': str(self.device.get_device_number()) or 'n/a',
            'device file': self.device.get_device_file() or 'n/a',
            'device file symlinks': ', '.join(self.device.get_device_file_symlinks()) or 'n/a',
            'number': self.device.get_number() or 'n/a',
        }

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
        return self.device.get_name() or '??'

    def __eq__(self, dev):
        if dev == None:
            return False
        else:
            return self.path == dev.path

class USBDevice(Device):
    @property
    def nice_label(self):
        if not 'TYPE' in self.device.get_property_keys():
            return self.device.get_name() or UNKNOWN_DEV

        usb_type = map(int, self.device.get_property('TYPE').split('/'))

        short_name, long_name = get_usb_short_long_names(usb_type[0], 
            usb_type[1], usb_type[2])

        return short_name

class PCIDevice(Device):
    def __get_class_subclass_protocol(self, pci_id):
        pci_protocol = int(pci_id[-2:], 16)
        pci_subclass = int(pci_id[-4:-2], 16)
        pci_class = int(pci_id[:-4], 16)
        return pci_class, pci_subclass, pci_protocol

    @property
    def nice_label(self):
        if not 'PCI_CLASS' in self.device.get_property_keys():
            return self.device.get_name() or UNKNOWN_DEV

        #FIXME: Check len(PCI_CLASS) = 5 | 6 first
        pci_class, pci_subclass, pci_protocol = \
            self.__get_class_subclass_protocol(str(self.device.get_property('PCI_CLASS')))

        short_name, long_name = get_pci_short_long_names(pci_class, 
            pci_subclass, pci_protocol)

        return short_name

class DeviceFinder(gobject.GObject):
    '''
    An object that will find and monitor Wiimote devices on your 
    machine and emit signals when are connected / disconnected
    '''
    
    __gsignals__ = {
        'connected': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT,)),
        'disconnected': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
            (gobject.TYPE_PYOBJECT,)),
    }
    
    def __init__(self, subsystems=['*']):
        '''
        Create a new DeviceFinder and attach to the udev system to 
        listen for events.
        '''
        self.__gobject_init__()

        self.client = gudev.Client(subsystems)
        self.subsystems = subsystems
        self.devices_tree = {}
        self.devices_list = []

        def explore_parent(device, devices_tree, devices_list):
            path = device.get_sysfs_path()        
            parent = device.get_parent()

            if parent:
                explore_parent(parent, devices_tree, devices_list)
                devices_tree[path] = self.get_device_object(device)
            else:
                devices_tree[path] = self.get_device_object(device)
                
            dev = self.get_device_object(device)
            if not dev in devices_list:
                devices_list.append(dev)

        for subsystem in subsystems:
            for device in self.client.query_by_subsystem(subsystem):
                explore_parent(device, self.devices_tree, self.devices_list)
                #FIXME: Devices needs a creation factory pattern
                """
                self.devices_list.append(dev)
                self.devices_tree[dev.path] = dev
                """

        self.client.connect('uevent', self.event)

    def get_device_object(self, device):
        #FIXME: Devices needs a creation factory pattern
        subsys = device.get_subsystem()
        if subsys == 'usb':
            dev = USBDevice(device)
        elif subsys == 'pci':
            dev = PCIDevice(device)
        else:
            dev = Device(device)
        
        return dev

    def get_devices_tree(self):
        return self.devices_tree
        
    def get_devices(self):
        return self.devices_list
        #return [device_tuple[0] for sysfs_path, device_tuple in self.devices.items()]

    def event(self, client, action, device):
        '''Handle a udev event'''
        
        return {
            'add': self.device_added,
#            'change': self.device_changed,
#            'remove': self.device_removed,
        }.get(action, lambda x,y: None)(device, device.get_subsystem())

    def device_added(self, device, subsystem):
        '''Called when a device has been added to the system'''
        
        print device, subsystem
        
        path = device.get_sysfs_path()
        self.devices_tree[path] = Device(device)
        self.devices_list.append(Device(device))
        self.emit('connected', device)

gobject.type_register(DeviceFinder)

if __name__ == '__main__':
    import gobject
    
    def found(finder, device):
        print device.path + ': ' + device.nice_label
    
    def lost(finder, device):
        print device.path + ': ' + device.nice_label
    
    finder = DeviceFinder()
    finder.connect('connected', found)
    finder.connect('disconnected', lost)
    
    import pprint
    pprint.pprint(finder.devices_tree)
    
    loop = gobject.MainLoop()
    loop.run()
