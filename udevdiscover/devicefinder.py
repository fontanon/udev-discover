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

from gi.repository import GObject
from gi.repository import GUdev
import device 

def get_subsystems():
    client = GUdev.Client()
    subsys = []

    for device in client.query_by_subsystem('*'):
        device_subsystem = device.get_subsystem()
        if not device_subsystem in subsys:
            subsys.append(device_subsystem)

    return subsys

class DeviceFinder(GObject.GObject):
    '''
    An object that will find and monitor devices on your 
    machine and emit signals when are added / removed / changed
    '''

    __gsignals__ = {
        'added': (GObject.SignalFlags.RUN_LAST, None, 
            (GObject.TYPE_PYOBJECT,)),
        'removed': (GObject.SignalFlags.RUN_LAST, None, 
            (GObject.TYPE_PYOBJECT,)),
        'changed': (GObject.SignalFlags.RUN_LAST, None, 
            (GObject.TYPE_PYOBJECT,)),
    }

    def __init__(self, subsystems='', parent_tree=False):
        '''
        Create a new DeviceFinder and attach to the udev system to 
        listen for events.
        '''
        GObject.GObject.__init__(self)

        self.client = GUdev.Client()
        self.subsystems = subsystems
        self.parent_tree = parent_tree
        self.devices_tree = {}
        self.devices_list = []

        self.client.connect('uevent', self.event)

    def scan_subsystems(self, subsystems='', parent_tree=False):
        self.client = GUdev.Client()
        self.subsystems = subsystems
        self.devices_tree = {}
        self.devices_list = []

        if subsystems == '': subsystems = ['*']
        for subsystem in subsystems:
            for gudevice in self.client.query_by_subsystem(subsystem):
                if parent_tree: 
                    self.__explore_parent(gudevice, self.devices_tree, 
                        self.devices_list)
                else:
                    self.devices_list.append(device.get_device_object(gudevice))
                    self.devices_tree[gudevice.get_sysfs_path()] = \
                        device.get_device_object(gudevice)

        self.client.connect('uevent', self.event)
        self.parent_tree = parent_tree

    def __explore_parent(self, gudevice, devices_tree, devices_list, emit=False):
        path = gudevice.get_sysfs_path()
        parent = gudevice.get_parent()

        if parent: 
            self.__explore_parent(parent, devices_tree, devices_list, emit)

        if not devices_tree.has_key(path):
            dev = device.get_device_object(gudevice)
            devices_tree[path] = dev
            devices_list.append(dev)

            if emit:
                self.emit('added', dev)

    def get_devices_tree(self):
        return self.devices_tree

    def get_devices(self):
        return self.devices_list

    def event(self, client, action, gudevice):
        '''Handle a udev event'''

        return {
            'add': self.device_added,
            'remove': self.device_removed,
            'change': self.device_changed,
        }.get(action, lambda x,y: None)(gudevice, gudevice.get_subsystem())

    def device_added(self, gudevice, subsystem):
        '''Called when a device has been added to the system'''

        dev = device.get_device_object(gudevice)

        if self.parent_tree: 
            self.__explore_parent(gudevice, self.devices_tree, self.devices_list, True)
        else:
            self.devices_list.append(dev)
            self.devices_tree[dev.path] = dev
            self.emit('added', dev)

    def device_removed(self, gudevice, subsystem):
        '''Called when a device has been removed from the system'''

        dev = device.get_device_object(gudevice)

        if dev in self.devices_list: self.devices_list.remove(dev)
        if self.devices_tree.has_key(dev.path): del(self.devices_tree[dev.path])

        self.emit('removed', dev)

    def device_changed(self, gudevice, subsystem):
        '''Called when a device has been updated'''

        dev = device.get_device_object(gudevice)
        self.emit('changed', dev)

GObject.type_register(DeviceFinder)

if __name__ == '__main__':
    import pprint
    from gi.repository import GObject

    def found(finder, device):
        print 'Added', device.path + ': ' + device.nice_label

    def lost(finder, device):
        print 'Removed', device.path + ': ' + device.nice_label

    def changes(finder, device):
        print 'Changed', device.path + ': ' + device.nice_label

    finder = DeviceFinder()
    pprint.pprint(finder.get_subsystems())

    finder.connect('added', found)
    finder.connect('removed', lost)
    finder.connect('changed', changes)

    finder.scan_subsystems()
    pprint.pprint(finder.devices_list)

    loop = GObject.MainLoop()
    loop.run()
