#!/usr/bin/env python3

# QinHeng Electronics CH-340 / HL-340 USB relay fan controller script

# By Dan MacDonald, 2021

# You must install the python USB modules to run this:

# sudo apt install python-usb
# or
# pacman -S python-pyusb

# To run with pyusb debugging:
#
#   PYUSB_DEBUG=debug python relay.py

import subprocess, time, usb.core, usb.util

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


ON_THRESHOLD = 80  # (degrees Celsius) Fan kicks on at this temperature
OFF_THRESHOLD = 70  # (degress Celsius) Fan shuts off at this temperature
SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature


# function to get the CPU temp
def getCPUTemp():
	f = open("/sys/class/thermal/thermal_zone0/temp")
	CPUTemp = f.read()
	f.close()
	return int(CPUTemp.replace("\n",""))/1000	# remove return from result, cast to int and divide by 1000


if __name__ == '__main__':
    # Validate the on and off thresholds
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    while True:
        temp = getCPUTemp()
        
        # print ("CPU temperature: %d" % (temp))

        # Start the fan if the temperature has reached the limit
        if temp > ON_THRESHOLD:
            ep.write(close_relay_cmd)
        #    print ("Starting fan")

        # Stop the fan if the off threshold is reached
        elif temp < OFF_THRESHOLD:
            ep.write(open_relay_cmd)
        #    print ("Stopping fan")

        time.sleep(SLEEP_INTERVAL)
