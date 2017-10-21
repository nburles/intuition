# intuition [![Build Status](https://travis-ci.org/shortbloke/intuition.svg?branch=dev)](https://travis-ci.org/shortbloke/intuition) 

Python asyncio library for receiving multicast UDP (local) messages from the Network Owl (OWL Intution) home energy monitor.

This library does not interface with the Owl Intuition website, and requires that it be run on the same LAN segment as the Network Owl.

- Copyright 2017 Martin Rowan
- Copyright 2013-2014 Michael Farrell <micolous+git@gmail.com>
- Copyright 2013 Johan van den Dorpe <johan.vandendorpe@gmail.com>

Licensed under the GNU LGPL3+.  For more details see `COPYING` and `COPYING.LESSER`.

## Requirements ##

- Python 3.5 or later

## Owl Protocol Support ##

This only supports receiving information from a Network Owl over multicast UDP.

It supports the following packet types:

- Electricity usage monitoring
- Solar
- Heating (protcol version 2.3 and later)
- Hot Water (protcol version 2.3 and later)
- Weather (Note: There isn't a sensor in the owl device to provide this. The information is sourced from an Owl Web Service)

Other packet types are unsupported and ignored, but patches to implement it are welcome. You may need to update the firmware on your device, which can be done when logged into your [Owl Intuition Account](https://www.owlintuition.com/)

## Usage ##

Running `intuition\__init__.py` will run the module in test mode, where it will output parsed messages to the console window


### Example: rrd ###
You can use the `examples\rrd\` file to generate an rrd file to graph electricity usage information with `rrdtool`.

## Tests ##

<TO DO: Add outline of running tests manually and within travis>