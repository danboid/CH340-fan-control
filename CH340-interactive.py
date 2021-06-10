#!/usr/bin/env python3

# QinHeng Electronics CH-340 / HL-340 USB relay manual toggle script

# By Dan MacDonald, 2021

# You must install the python USB modules to run this:

# sudo apt install python-usb
# or
# pacman -S python-pyusb

# To run with pyusb debugging:
#
#   PYUSB_DEBUG=debug python relay.py

import os, sys, subprocess, usb.core, usb.util
 
# This script must be run as root!
if not os.geteuid()==0:
    sys.exit('This script must be run as root or as a sudo user.')
    
if len(sys.argv) != 2:
    sys.exit('You must provide an option, -on or -off')

dev = usb.core.find(idVendor=0x1a86, idProduct=0x7523)

if dev is None:
	raise ValueError("Device not found")

if dev.is_kernel_driver_active(0):
	dev.detach_kernel_driver(0)

cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

close_relay_cmd = [0xA0, 0x01, 0x01, 0xA2]
open_relay_cmd = [0xA0, 0x01, 0x00, 0xA1]

if __name__ == '__main__':
    if sys.argv[1] == '-on':
        ep.write(close_relay_cmd)
        
    elif sys.argv[1] == '-off':
        ep.write(open_relay_cmd)
        
    else: 
        print('Unknown option', sys.argv[1])
