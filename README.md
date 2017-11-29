# intuition 
[![Build Status](https://travis-ci.org/shortbloke/intuition.svg?branch=dev)](https://travis-ci.org/shortbloke/intuition)
[![Coverage Status](https://coveralls.io/repos/github/shortbloke/intuition/badge.svg?branch=dev)](https://coveralls.io/github/shortbloke/intuition?branch=dev)

Python asyncio library for receiving messages from the Network Owl (OWL Intution) home energy monitor. Supports messages being multicast on LAN and via directed UDP.

This library does not interface with the Owl Intuition website, and requires that it be run on the same LAN segment as the Network Owl.

- Copyright 2017 Martin Rowan <martin+github@rowannet.co.uk>
- Copyright 2013-2014 Michael Farrell <micolous+git@gmail.com>
- Copyright 2013 Johan van den Dorpe <johan.vandendorpe@gmail.com>

Licensed under the GNU LGPL3+.  For more details see `COPYING` and `COPYING.LESSER`.

## Requirements ##

- Python 3.5 or later

## Owl Protocol Support ##

It supports the following packet types:

- Electricity usage monitoring
- Solar
- Heating (protcol version 2.3 and later)
- Hot Water (protcol version 2.3 and later)
- Weather (Note: There isn't a sensor in the owl device to provide this. The information is sourced from an Owl Web Service)

Other packet types are unsupported and ignored, but patches to implement it are welcome. You may need to update the firmware on your device, which can be done when logged into your [Owl Intuition Account](https://www.owlintuition.com/)

It supports two methods of receiving messages as defined in: [Multicast & UDP API Information] (https://theowl.zendesk.com/hc/en-gb/articles/201284603-Multicast-UDP-API-Information)
- Multicast (PUSH) (default)
- UDP (PUSH)

## Usage ##

Calling this module can be performed from the following function:
- start_listening - To use the asyncio socket listen to receive messages
- parse_datagram - To directly parse a receive xml message

Running `intuition\protocol.py` will run the module in test mode, where it will output parsed messages to the console window. 

The command line arguments are passed to start_listening function which supports:
- '-i \<interface\>' - To specficfy a specific network interface to listen on.
- '-u' - To specify UDP (PUSH) listening mode.
- '-p \<portnumber\>' - To specify the UDP (PUSH) listening port number (default 32000).


### Example: rrd ###
You can use the `examples\rrd\` file to generate an rrd file to graph electricity usage information with `rrdtool`.

## Tests ##

TO DO: Add outline of running tests manually and within travis
