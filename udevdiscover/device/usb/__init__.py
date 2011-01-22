# -*- coding: utf-8 -*-
# vim: ts=4 
###
#
# Copyright (c) 2010 J. Félix Ontañón
#
# usb_class_names adapted from gnome-device-manager
# Copyright (C) 2007 David Zeuthen
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

import subprocess
import re

from udevdiscover.device import Device
from udevdiscover.utils import memoized

UNKNOWN_NAME = 'Unknown USB Device'
USB_DB_CMD = '/lib/udev/usb-db'

vendor_regex = re.compile('(?<=ID_VENDOR_FROM_DATABASE=).*')
model_regex = re.compile('(?<=ID_MODEL_FROM_DATABASE=).*')

usb_class_names = {
    (0x01,   -1,   -1): (_('Audio'), _('Audio')),
    (0x01, 0x01,   -1): (_('Audio Control'), _('Audio Control')),
    (0x01, 0x02,   -1): (_('Audio Streaming'), _('Audio Streaming')),
    (0x01, 0x03,   -1): (_('Audio MIDI Streaming'), _('Audio MIDI Streaming')),

    (0x02,   -1,   -1): (_('Communications'), _('Communications')),
    (0x02, 0x01,   -1): (_('Direct Line'), _('Direct Line Communications')),
    (0x02, 0x02,   -1): (_('Modem'), _('Modem Communications')),
    (0x02, 0x02, 0x01): (_('Modem (AT v.25ter)'), _('Modem (AT v.25ter) Communications')),
    (0x02, 0x02, 0x02): (_('Modem (PCCA101)'), _('Modem (PCCA101) Communications')),
    (0x02, 0x02, 0x03): (_('Modem (PCCA101)'), _('Modem (PCCA101 + wakeup) Communications')),
    (0x02, 0x02, 0x04): (_('Modem (GSM)'), _('Modem (GSM) Communications')),
    (0x02, 0x02, 0x05): (_('Modem (3G)'), _('Modem (3G) Communications')),
    (0x02, 0x02, 0x06): (_('Modem (CDMA)'), _('Modem (CDMA) Communications')),
    (0x02, 0x02, 0xfe): (_('Modem'), _('Modem (Defined by command set descriptor) Communications')),
    (0x02, 0x02, 0xff): (_('Modem (Vendor Specific)'), _('Modem (Vendor Specific) Communications')),
    (0x02, 0x03,   -1): (_('Telephone'), _('Telephone Communications')),
    (0x02, 0x04,   -1): (_('Multi-Channel'), _('Multi-Channel Communications')),
    (0x02, 0x05,   -1): (_('CAPI Control'), _('CAPI Control')),
    (0x02, 0x06,   -1): (_('Ethernet Networking'), _('Ethernet Networking')),
    (0x02, 0x07,   -1): (_('ATM Networking'), _('ATM Networking')),
    (0x02, 0x08,   -1): (_('Wireless Handset Control'), _('Wireless Handset Control')),
    (0x02, 0x09,   -1): (_('Device Management'), _('Device Management')),
    (0x02, 0x0a,   -1): (_('Mobile Direct Line'), _('Mobile Direct Line')),
    (0x02, 0x0b,   -1): (_('OBEX'), _('OBEX')),
    (0x02, 0x0c,   -1): (_('Ethernet Emulation'), _('Ethernet Emulation')),
    (0x02, 0x0c, 0x07): (_('Ethernet Emulation'), _('Ethernet Emulation (EEM)')),

    (0x03,   -1,   -1): (_('HID Device'), _('HID Device')),
    (0x03,   -1, 0x00): (_('HID Device'), _('HID Device')),
    (0x03,   -1, 0x01): (_('Keyboard HID Device'), _('Keyboard HID Device')),
    (0x03,   -1, 0x02): (_('Mouse HID Device'), _('Mouse HID Device ')),
    (0x03, 0x01, 0x00): (_('HID Device'), _('HID Device Interface (Boot)')),
    (0x03, 0x01, 0x01): (_('Keyboard HID Device'), _('Keyboard HID Device Interface (Boot)')),
    (0x03, 0x01, 0x02): (_('Mouse HID Device'), _('Mouse HID Device Interface (Boot)')),

    (0x06,   -1,   -1): (_('Imaging Device'), _('Imaging Device')),
    (0x06, 0x01,   -1): (_('Still Image Capture'), _('Still Image Capture')),
    (0x06, 0x01, 0x01): (_('PTP Imaging Device'), _('PTP Imaging Device')),

    (0x07,   -1,   -1): (_('Printer'), _('Printing')),
    (0x07, 0x01, 0x01): (_('Printer'), _('Printing Interface (Unidirectional)')),
    (0x07, 0x01, 0x01): (_('Printer'), _('Printing Interface (Bidirectional)')),
    (0x07, 0x01, 0x01): (_('Printer'), _('Printing Interface (IEEE 1284.4 Compatible Bidirectional)')),
    (0x07, 0x01, 0xff): (_('Printer'), _('Printing Interface (Vendor Specific)')),

    (0x08,   -1,   -1): (_('USB Mass Storage'), _('USB Mass Storage')),
    (0x08, 0x01,   -1): (_('USB Mass Storage'), _('USB Mass Storage (Flash)')),
    (0x08, 0x02,   -1): (_('USB Mass Storage'), _('USB Mass Storage (SFF-8020i, MMC-2 (ATAPI))')),
    (0x08, 0x03,   -1): (_('USB Mass Storage'), _('USB Mass Storage (QIC-157)')),
    (0x08, 0x04,   -1): (_('USB Mass Storage'), _('USB Mass Storage (Floppy (UFI))')),
    (0x08, 0x05,   -1): (_('USB Mass Storage'), _('USB Mass Storage (SFF-8070i)')),
    (0x08, 0x06,   -1): (_('USB Mass Storage'), _('USB Mass Storage (SCSI)')),

    (0x09,   -1,   -1): (_('Hub'), _('Hub')),
    (0x09, 0x00, 0x00): (_('Hub'), _('Hub')),
    (0x09, 0x00, 0x01): (_('Hub'), _('Hub Interface (Single TT)')),
    (0x09, 0x00, 0x02): (_('Hub'), _('Hub Interface (TT per port)')),

    (0x0a,   -1,   -1): (_('CDC Data'), _('CDC Data')),
    (0x0a,   -1, 0x31): (_('HDLC Data'), _('HDLC Data')),
    (0x0a,   -1, 0x32): (_('Transparent Data'), _('Transparent Data')),
    (0x0a,   -1, 0x50): (_('Q.921M Data'), _('Q.921M Data')),
    (0x0a,   -1, 0x51): (_('Q.921 Data'), _('Q.921 Data')),
    (0x0a,   -1, 0x52): (_('Q.921TM Data'), _('Q.921TM Data')),
    (0x0a,   -1, 0x90): (_('V.42bis Data'), _('V.42bis Data')),
    (0x0a,   -1, 0x91): (_('Q.932 EuroISDN Data'), _('Q.932 EuroISDN Data')),
    (0x0a,   -1, 0x92): (_('V.120 V.24 rate ISDN Data'), _('V.120 V.24 rate ISDN Data')),
    (0x0a,   -1, 0x93): (_('CAPI 2.0 Data'), _('CAPI 2.0 Data')),
    (0x0a,   -1, 0xfd): (_('Host Based Data Driver'), _('Host Based Driver Data')),
    (0x0a,   -1, 0xfe): (_('CDC PUF Data'), _('CDC PUF Data')),
    (0x0a,   -1, 0xff): (_('Vendor Specific Data'), _('Vendor Specific Data')),

    (0x0b,   -1,   -1): (_('Chip / Smart Card'), _('Chip / Smart Card')),

    (0x0d,   -1,   -1): (_('Content Security'), _('Content Security')),

    (0x0e,   -1,   -1): (_('Video'), _('Video')),
    (0x0e, 0x01,   -1): (_('Video Control'), _('Video Control')),
    (0x0e, 0x02,   -1): (_('Video Streaming'), _('Video Streaming')),
    (0x0e, 0x03,   -1): (_('Video Interface Collection'), _('Video Interface Collection')),

    (0xdc,   -1,   -1): (_('Diagnostics'), _('Diagnostics')),

    (0xe0,   -1,   -1): (_('Wireless Adapter'), _('Wireless Adapter')),
    (0xe0, 0x01,   -1): (_('Wireless Radio'), _('Wireless Radio')),
    (0xe0, 0x01, 0x01): (_('Bluetooth Adapter'), _('Bluetooth Adapter')),
    (0xe0, 0x01, 0x02): (_('Ultra Wideband Radio Control'), _('Ultra Wideband Radio Control')),
    (0xe0, 0x01, 0x03): (_('RNDIS'), _('RNDIS')),
    (0xe0, 0x02,   -1): (_('Wireless USB Wire Adapter'), _('Wireless USB Wire Adapter')),
    (0xe0, 0x02, 0x01): (_('Wireless USB Wire Adapter'), _('Host Wire Adapter Control/Data Streaming')),
    (0xe0, 0x02, 0x02): (_('Wireless USB Wire Adapter'), _('Device Wire Adapter Control/Data Streaming')),
    (0xe0, 0x02, 0x03): (_('Wireless USB Wire Adapter'), _('Device Wire Adapter Isochronous Streaming')),

    (0xef,   -1,   -1): (_('Miscellanous'), _('Miscellanous')),
    (0xef, 0x01, 0x01): (_('MS ActiveSync'), _('MS ActiveSync')),
    (0xef, 0x01, 0x02): (_('Palm Sync'), _('Palm Sync')),
    (0xef, 0x02,   -1): (_('Miscellanous Common'), _('Miscellanous Common')),
    (0xef, 0x02, 0x01): (_('Interface Association'), _('Interface Association')),
    (0xef, 0x02, 0x02): (_('Wire Adapter Multifunction'), _('Wire Adapter Multifunction Peripheral')),
    (0xef, 0x03, 0x01): (_('Cable Based Association'), _('Cable Based Association')),

    (0xfe,   -1,   -1): (_('Application Specific'), _('Application Specific')),
    (0xfe, 0x01,   -1): (_('Device Firmware Update'), _('Device Firmware Update')),
    (0xfe, 0x02,   -1): (_('IRDA Bridge'), _('IRDA Bridge')),
    (0xfe, 0x03,   -1): (_('Test and Measurement'), _('Test and Measurement')),
    (0xfe, 0x03, 0x01): (_('TMC Test and Measurement'), _('TMC Test and Measurement')),
    (0xfe, 0x03, 0x02): (_('USB488 Test and Measurement'), _('USB488 Test and Measurement')),
}

def get_device_object(device):
    devtype = device.get_devtype()
    
    if devtype == 'usb_interface':
        return USBInterface(device)
    else:
        return USBDevice(device)

@memoized
def get_usb_short_long_names(usb_class, usb_subclass, usb_protocol):
    key = [usb_class]

    klasses = [k for k in usb_class_names.keys() if k[0] == usb_class]
    if not klasses:
        return None, None

    subklasses = [s for s in klasses if s[1] == usb_subclass]
    
    if not subklasses:
        key.append(-1)
    else:
        key.append(usb_subclass)

    if not (key[0], key[1], usb_protocol) in klasses:
        key.append(-1)
    else:
        key.append(usb_protocol)

    return usb_class_names[tuple(key)]

@memoized
def get_usb_vendor_model_names(sysfs_path):
    vendor_name, model_name = None, None

    process = subprocess.Popen([USB_DB_CMD, sysfs_path], stdout=subprocess.PIPE)
    if process.wait() == 0:
        output = process.communicate()[0]
        vendor_res = vendor_regex.search(output)
        model_res = model_regex.search(output)
        if vendor_res: vendor_name = vendor_res.group(0)
        if model_res: model_name = model_res.group(0)

    return vendor_name, model_name

class USBDevice(Device):
    @property
    def nice_label(self):
        usb_type = map(int, self.device.get_property('TYPE').split('/'))

        short_name, long_name = get_usb_short_long_names(usb_type[0], 
            usb_type[1], usb_type[2])

        if not short_name:
            return 'USB Device'

        return short_name

    @property
    def vendor_name(self):
        return self.device.get_property('ID_VENDOR') or \
            get_usb_vendor_model_names(self.path.split('/sys')[1])[0]

    @property
    def model_name(self):
        return self.device.get_property('ID_MODEL') or \
            get_usb_vendor_model_names(self.path.split('/sys')[1])[1]

class USBInterface(Device):
    @property
    def nice_label(self):
        usb_type = map(int, self.device.get_property('INTERFACE').split('/'))

        short_name, long_name = get_usb_short_long_names(usb_type[0], 
            usb_type[1], usb_type[2])

        if not short_name:
            return 'USB Interface'

        return "%s Interface" % short_name
