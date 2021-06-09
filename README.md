# CH340-fan-control


## What is this?

This repo contains a python script to control a USB fan with the QinHeng Electronics CH340/HL340 USB relay module under Linux. I have only tested it with the CH340.

It will turn a USB powered fan off when a given temp is exceeded (the default is 80 degrees C) and turn it off when it falls below a lower threshold value, defaulting to 70 degrees C.


## What is it for?

I own a few Android TV boxes that have poor thermal designs that are prone to overheating when under sustained load. This can either cause your device to significantly slow down or shut down entirely. This can be fixed by cutting a hole in the bottom on your TV box above the SoC and sticking a small USB fan on it. In my case I am using a AC Infinity 40mm x 20mm USB Fan that cost me £10. 

Fans can be annoying if they're always on so you can use this script in conjunction with a QinHeng Electronics CH340/HL340 based USB relay module, mine cost me £5, to only activate the fan when it is required. My CH340 is badged as a SONGLE but I've seen similar devices badged as Mogzank or HALJIA 5V USB relay modules or controllers.


## How do I wire up my USB fan to the relay adapter?

Connect the grey (or red) wire from the fan into the COM (middle) terminal of the relay module and connect the grey (or red) wire of the USB header to the NO terminal of the relay. No soldering is required, it is usually enough to screw the wires into the terminals.


## How do I install and run this script?

This script requires Python 3 and the Python USB modules. You almost certainly already have Python 3 installed already. To install the USB modules run:

```
$ sudo apt install python-usb
```
Under Ubuntu and Debian based distros or:

```
# pacman -S python-pyusb
```

Under Arch and Manjaro.

Copy `CH340-fan-control.py` into `/usr/local/bin` and copy `CH340-fan-control.service` into `/etc/systemd/system` and make sure its executable with:

```
$ sudo chmod u+x /etc/systemd/system/CH340-fan-control.service
```

Start the service:

```
$ sudo systemctl start CH340-fan-control
```

Enable it to run at boot:

```
$ sudo systemctl enable CH340-fan-control
```
