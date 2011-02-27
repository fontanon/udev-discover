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
    devname = gudevice.get_name()
    
    if devname.startswith('card'):
        return SoundCardDevice(gudevice)
    elif devname in ('timer', 'seq', 'sequencer'):
        return SystemSoundDevice(gudevice)
    else:
        return SoundDevice(gudevice)

class SoundCardDevice(Device):
    DEFAULT_ICON = 'audio-card'

    @property
    def nice_label(self):
        if self.device.has_property('SOUND_FORM_FACTOR'):
            return _('%s Sound Card') % \
                self.device.get_property('SOUND_FORM_FACTOR').capitalize()
        else:
            return _('Sound Card')

    @property
    def vendor_name(self):
        return self.device.get_property('ID_VENDOR_FROM_DATABASE')

    @property
    def model_name(self):
        return self.device.get_property('ID_MODEL_FROM_DATABASE')

class SystemSoundDevice(Device):
    DEFAULT_ICON = 'audio-card'

    @property
    def nice_label(self):
        devname = self.device.get_name()

        return {
            'timer': _('Sound Timer'),
            'seq': _('Sound Sequencer'),
            'sequencer': _('Sound Sequencer'),
        }.get(devname)

class SoundDevice(Device):
    DEFAULT_ICON = 'audio-input-microphone'

    def __init__(self, gudevice):
        super(SoundDevice, self).__init__(gudevice)

        devname = gudevice.get_name()

        if devname.startswith('controlC'):
            self.__type = 'control'
        elif devname.startswith('pcmC'):
            if devname.endswith('c'):
                self.__type = 'capture'
            elif devname.endswith('p'):
                self.__type = 'playback'
            else:
                self.__type = 'unknown'
        elif devname.startswith('hwC'):
            self.__type = 'hwspecific'
        elif devname.startswith('midiC'):
            self.__type = 'midi'
        else:
            self.__type = 'unknown'

    @property
    def nice_label(self):
        return {
            'control': _('Control Sound Device'),
            'capture': _('Capture Sound Device'),
            'playback': _('Playback Sound Device'),
            'hwspecific': _('HW Specific Sound Device'),
            'midi': _('MIDI Sound Device'),
            'unknown': _('Unknown Sound Device')
        }.get(self.type)

    @property
    def type(self):
        return self.__type
