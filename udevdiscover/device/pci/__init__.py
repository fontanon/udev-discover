# -*- coding: utf-8 -*-
# vim: ts=4 
###
#
# Copyright (c) 2010 J. Félix Ontañón
#
# pci_class_names adapted from gnome-device-manager
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

UNKNOWN_NAME = 'Unknown PCI Device'
PCI_DB_CMD = '/lib/udev/pci-db'

vendor_regex = re.compile('(?<=ID_VENDOR_FROM_DATABASE=).*')
model_regex = re.compile('(?<=ID_MODEL_FROM_DATABASE=).*')

pci_class_names = {
    (0x01,   -1,   -1): (_('Storage Controller'), _('Mass Storage Controller')),
    (0x01, 0x00,   -1): (_('SCSI Controller'), _('SCSI Storage Controller')),
    (0x01, 0x01,   -1): (_('IDE Controller'), _('IDE Storage Controller')),
    (0x01, 0x02,   -1): (_('Floppy Controller'), _('Floppy Disk Storage Controller')),
    (0x01, 0x03,   -1): (_('IPI Controller'), _('IPI Bus Storage Controller')),
    (0x01, 0x04,   -1): (_('RAID Controller'), _('Raid Bus Storage Controller')),
    (0x01, 0x05,   -1): (_('ATA Controller'), _('ATA Storage Controller')),
    (0x01, 0x06,   -1): (_('SATA Controller'), _('SATA Storage Controller')),
    (0x01, 0x06, 0x01): (_('AHCI Controller'), _('SATA ACHI 1.0 Storage Controller')),
    (0x01, 0x07,   -1): (_('Serial SCSI Controller'), _('Serial SCSI Storage Controller')),

    (0x02,   -1,   -1): (_('Network Controller'), _('Network Controller')),
    (0x02, 0x00,   -1): (_('Ethernet Controller'), _('Ethernet Network Controller')),
    (0x02, 0x01,   -1): (_('Token Ring Controller'), _('Token Ring Network Controller')),
    (0x02, 0x02,   -1): (_('FDDI Controller'), _('FDDI Network Controller')),
    (0x02, 0x03,   -1): (_('ATM Controller'), _('ATM Network Controller')),
    (0x02, 0x03,   -1): (_('ISDN Controller'), _('ISDN Network Controller')),

    (0x03,   -1,   -1): (_('Display Controller'), _('Display Controller')),
    (0x03, 0x00,   -1): (_('VGA Controller'), _('VGA Controller')),
    (0x03, 0x01,   -1): (_('XGA Controller'), _('XGA Controller')),
    (0x03, 0x02,   -1): (_('3D Controller'), _('3D Controller')),

    (0x04,   -1,   -1): (_('Multimedia Controller'), _('Multimedia Controller')),
    (0x04, 0x00,   -1): (_('Video Controller'), _('Video Controller')),
    (0x04, 0x01,   -1): (_('Audio Controller'), _('Audio Controller')),
    (0x04, 0x02,   -1): (_('Telephony Controller'), _('Telephony Controller')),
    (0x04, 0x03,   -1): (_('Audio Device'), _('Audio Device')),

    (0x05,   -1,   -1): (_('Memory Controller'), _('Memory Controller')),
    (0x05, 0x00,   -1): (_('RAM Controller'), _('RAM Memory Controller')),
    (0x05, 0x01,   -1): (_('FLASH Controller'), _('FLASH Memory Controller')),

    (0x06,   -1,   -1): (_('Bridge'), _('Bridge')),
    (0x06, 0x00,   -1): (_('Host Bridge'), _('Host Bridge')),
    (0x06, 0x01,   -1): (_('ISA Bridge'), _('ISA Bridge')),
    (0x06, 0x02,   -1): (_('EISA Bridge'), _('EISA Bridge')),
    (0x06, 0x03,   -1): (_('MicroChannel Bridge'), _('MicroChannel Bridge')),
    (0x06, 0x04,   -1): (_('PCI Bridge'), _('PCI Bridge')),
    (0x06, 0x04, 0x00): (_('PCI Bridge'), _('PCI Bridge (Normal decode)')),
    (0x06, 0x04, 0x01): (_('PCI Bridge'), _('PCI Bridge (Subtractive decode)')),
    (0x06, 0x05,   -1): (_('PCMCIA Bridge'), _('PCMCIA Bridge')),
    (0x06, 0x06,   -1): (_('NuBus Bridge'), _('NuBus Bridge')),
    (0x06, 0x07,   -1): (_('CardBus Bridge'), _('CardBus Bridge')),
    (0x06, 0x08,   -1): (_('RACEway Bridge'), _('RACEway Bridge')),
    (0x06, 0x09,   -1): (_('Semitrans. PCI-to-PCI Bridge'), _('Semitransparent PCI-to-PCI Bridge')),
    (0x06, 0x0a,   -1): (_('InfiniBand to PCI Host Bridge'), _('InfiniBand to PCI Host Bridge')),

    (0x07,   -1,   -1): (_('Communications Controller'), _('Communications Controller')),
    (0x07, 0x00,   -1): (_('Serial Controller'), _('Serial Controller')),
    (0x07, 0x00, 0x00): (_('8250 Serial Controller'), _('8540 Serial Controller')),
    (0x07, 0x00, 0x00): (_('16450 Serial Controller'), _('16450 Serial Controller')),
    (0x07, 0x00, 0x00): (_('16550 Serial Controller'), _('16550 Serial Controller')),
    (0x07, 0x00, 0x00): (_('16650 Serial Controller'), _('16650 Serial Controller')),
    (0x07, 0x00, 0x00): (_('16750 Serial Controller'), _('16750 Serial Controller')),
    (0x07, 0x00, 0x00): (_('16850 Serial Controller'), _('16850 Serial Controller')),
    (0x07, 0x00, 0x00): (_('16950 Serial Controller'), _('16950 Serial Controller')),
    (0x07, 0x01,   -1): (_('Parallel Controller'), _('Parallel Controller')),
    (0x07, 0x01, 0x00): (_('SPP Parallel Controller'), _('SPP Parallel Controller')),
    (0x07, 0x01, 0x01): (_('Bidir Parallel Controller'), _('Bidirectional Parallel Controller')),
    (0x07, 0x01, 0x02): (_('ECP Parallel Controller'), _('ECP Parallel Controller')),
    (0x07, 0x01, 0x03): (_('IEEE 1284 Parallel Controller'), _('IEEE 1284 Parallel Controller')),
    (0x07, 0x01, 0xfe): (_('IEEE 1284 Target Parallel Controller'), _('IEEE 1284 Target Parallel Controller')),
    (0x07, 0x02,   -1): (_('Multiport Serial Controller'), _('Multiport Serial Controller')),
    (0x07, 0x03,   -1): (_('Modem'), _('Modem')),
    (0x07, 0x03, 0x00): (_('Generic Modem'), _('Generic Modem')),
    (0x07, 0x03, 0x01): (_('Hayes/16450 Modem'), _('Hayes/16450 Compatiable Modem')),
    (0x07, 0x03, 0x02): (_('Hayes/16550 Modem'), _('Hayes/16550 Compatiable Modem')),
    (0x07, 0x03, 0x03): (_('Hayes/16650 Modem'), _('Hayes/16650 Compatiable Modem')),
    (0x07, 0x03, 0x04): (_('Hayes/16750 Modem'), _('Hayes/16750 Compatiable Modem')),

    (0x08,   -1,   -1): (_('System Peripheral'), _('Generic System Peripheral')),
    (0x08, 0x00,   -1): (_('PIC'), _('PIC System Peripheral')),
    (0x08, 0x00, 0x00): (_('8259 PIC'), _('8259 PIC System Peripheral')),
    (0x08, 0x00, 0x01): (_('ISA PIC'), _('ISA PIC System Peripheral')),
    (0x08, 0x00, 0x02): (_('EISA PIC'), _('EISA PIC System Peripheral')),
    (0x08, 0x00, 0x10): (_('IO-APIC'), _('IO-APIC System Peripheral')),
    (0x08, 0x00, 0x20): (_('IO(X)-APIC'), _('IO(X)-APIC System Peripheral')),
    (0x08, 0x01,   -1): (_('DMA Controller'), _('DMA Controller')),
    (0x08, 0x01, 0x00): (_('8237 DMA Controller'), _('DMA Controller')),
    (0x08, 0x01, 0x01): (_('ISA DMA Controller'), _('ISA DMA Controller')),
    (0x08, 0x01, 0x02): (_('EISA DMA Controller'), _('EISA DMA Controller')),
    (0x08, 0x02,   -1): (_('Timer Controller'), _('Timer Controller')),
    (0x08, 0x02, 0x00): (_('8254 Timer Controller'), _('8254 Timer Controller')),
    (0x08, 0x02, 0x01): (_('ISA Timer Controller'), _('ISA Timer Controller')),
    (0x08, 0x02, 0x02): (_('EISA Timer Controller'), _('EISA Timer Controller')),
    (0x08, 0x03,   -1): (_('Real-Time Clock'), _('Real-Time Clock')),
    (0x08, 0x03, 0x00): (_('Generic Real-Time Clock'), _('Generic Real-Time Clock')),
    (0x08, 0x03, 0x01): (_('ISA Real-Time Clock'), _('ISA Real-Time Clock')),
    (0x08, 0x04,   -1): (_('PCI Hot-plug Controller'), _('PCI Hot-plug Controller')),

    (0x09,   -1,   -1): (_('Input Controller'), _('Input Device Controller')),
    (0x09, 0x00,   -1): (_('Keyboard Controller'), _('Keyboard Controller')),
    (0x09, 0x01,   -1): (_('Digitizer Pen Controller'), _('Digitizer Pen Controller')),
    (0x09, 0x02,   -1): (_('Mouse Controller'), _('Mouse Controller')),
    (0x09, 0x03,   -1): (_('Scanner Controller'), _('Scanner Controller')),
    (0x09, 0x04,   -1): (_('Gameport Controller'), _('Gameport Controller')),
    (0x09, 0x04, 0x00): (_('Gameport Controller'), _('Generic Gameport Controller')),
    (0x09, 0x04, 0x10): (_('Gameport Controller'), _('Extended Gameport Controller')),

    (0x0a,   -1,   -1): (_('Docking Station'), _('Docking Station')),
    (0x0a, 0x00,   -1): (_('Docking Station'), _('Generic Docking Station')),

    (0x0b,   -1,   -1): (_('Processor'), _('Processor')),
    (0x0b, 0x00,   -1): (_('386 Processor'), _('386 Processor')),
    (0x0b, 0x01,   -1): (_('486 Processor'), _('486 Processor')),
    (0x0b, 0x02,   -1): (_('Pentium Processor'), _('Pentium Processor')),
    (0x0b, 0x10,   -1): (_('Alpha Processor'), _('Alpha Processor')),
    (0x0b, 0x20,   -1): (_('Power PC Processor'), _('Power PC Processor')),
    (0x0b, 0x30,   -1): (_('MIPS Processor'), _('MIPS Processor')),
    (0x0b, 0x40,   -1): (_('Co-processor'), _('Co-processor')),

    (0x0c,   -1,   -1): (_('Serial Bus Controller'), _('Serial Bus Controller')),
    (0x0c, 0x00,   -1): (_('IEEE 1394 Controller'), _('IEEE 1394 Controller')),
    (0x0c, 0x00, 0x10): (_('IEEE 1394 OHCI Controller'), _('IEEE 1394 OHCI Controller')),
    (0x0c, 0x01,   -1): (_('ACCESS Bus Controller'), _('ACCESS Bus Controller')),
    (0x0c, 0x02,   -1): (_('SSA Controller'), _('SSA Controller')),
    (0x0c, 0x03,   -1): (_('USB Controller'), _('USB Controller')),
    (0x0c, 0x03, 0x00): (_('USB UHCI Controller'), _('USB UHCI Controller')),
    (0x0c, 0x03, 0x10): (_('USB OHCI Controller'), _('USB OHCI Controller')),
    (0x0c, 0x03, 0x20): (_('USB EHCI Controller'), _('USB EHCI Controller')),
    (0x0c, 0x04,   -1): (_('Fibre Channel Controller'), _('Fibre Channel Controller')),
    (0x0c, 0x05,   -1): (_('SMBus Controller'), _('SMBus Controller')),
    (0x0c, 0x06,   -1): (_('InfiniBand Controller'), _('InfiniBand Controller')),

    (0x0d,   -1,   -1): (_('Wireless Controller'), _('Wireless Controller')),
    (0x0d, 0x00,   -1): (_('IRDA Controller'), _('IRDA Wireless Controller')),
    (0x0d, 0x01,   -1): (_('Consumer IR Controller'), _('Consumer IR Wireless Controller')),
    (0x0d, 0x10,   -1): (_('RF Controller'), _('RF Wireless Controller')),

    (0x0e,   -1,   -1): (_('Intelligent Controller'), _('Intelligent Controller')),
    (0x0e,   -1,   -1): (_('I20 Controller'), _('I20 Intelligent Controller')),

    (0x0f,   -1,   -1): (_('Satellite Comm. Controller'), _('Satellite Communications Controller')),
    (0x0f, 0x00,   -1): (_('Satellite TV Controller'), _('Satellite TV Communications Controller')),
    (0x0f, 0x01,   -1): (_('Satellite Audio Controller'), _('Satellite Audio Communications Controller')),
    (0x0f, 0x03,   -1): (_('Satellite Voice Controller'), _('Satellite Voice Communications Controller')),
    (0x0f, 0x04,   -1): (_('Satellite Data Controller'), _('Satellite Data Communications Controller')),

    (0x10,   -1,   -1): (_('Encryption Controller'), _('Encryption Controller')),
    (0x10, 0x00,   -1): (_('Network Encryption Device'), _('Network and Computing Encryption Device')),

    (0x11,   -1,   -1): (_('Signal Processing Controller'), _('Signal Processing Controller')),
    (0x11, 0x00,   -1): (_('DPIO Module'), _('DPIO Module Signal Processing Controller')),
    (0x11, 0x01,   -1): (_('Performance Counters'), _('Performance Counters'))
}

def get_device_object(device):
    return PCIDevice(device)

@memoized
def get_pci_short_long_names(pci_class, pci_subclass, pci_protocol):
    key = [pci_class]

    klasses = [k for k in pci_class_names.keys() if k[0] == pci_class]
    if not klasses:
        return UNKNOWN_NAME, UNKNOWN_NAME

    subklasses = [s for s in klasses if s[1] == pci_subclass]
    
    if not subklasses:
        key.append(-1)
    else:
        key.append(pci_subclass)

    if not (key[0], key[1], pci_protocol) in klasses:
        key.append(-1)
    else:
        key.append(pci_protocol)

    return pci_class_names[tuple(key)]

@memoized
def get_pci_vendor_model_names(sysfs_path):
    vendor_name, model_name = None, None

    process = subprocess.Popen([PCI_DB_CMD, sysfs_path], stdout=subprocess.PIPE)
    if process.wait() == 0:
        output = process.communicate()[0]
        vendor_res = vendor_regex.search(output)
        model_res = model_regex.search(output)
        if vendor_res: vendor_name = vendor_res.group(0)
        if model_res: model_name = model_res.group(0)

    return vendor_name, model_name

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

    @property
    def vendor_name(self):
        return get_pci_vendor_model_names(self.path.split('/sys')[1])[0]

    @property
    def model_name(self):
        return get_pci_vendor_model_names(self.path.split('/sys')[1])[1]
