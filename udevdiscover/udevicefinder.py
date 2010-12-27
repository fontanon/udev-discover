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
from usb import USBDevice
from pci import PCIDevice
from device import Device

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
    
    def __init__(self, subsystems=['*'], parent_tree=False):
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
                if parent_tree: 
                    explore_parent(device, self.devices_tree, self.devices_list)
                else:
                    self.devices_list.append(self.get_device_object(device))
                    self.devices_tree[device.get_sysfs_path()] = \
                        self.get_device_object(device)

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
