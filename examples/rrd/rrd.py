"""
intuition/rrd.py - rrdtool integration support for OWL Intuition.
Copyright 2013 Michael Farrell <micolous+git@gmail.com>

This library is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this library.  If not, see <http://www.gnu.org/licenses/>.

"""

from __future__ import absolute_import
from argparse import ArgumentParser
from twisted.internet import reactor
import rrdtool
from intuition import OwlIntuitionProtocol, MCAST_PORT, OwlElectricity


class RrdOwlProtocol(OwlIntuitionProtocol):
    def __init__(self, src, rrd, *args, **kwargs):
        self.src = src
        self.rrd = rrd
        OwlIntuitionProtocol.__init__(self, *args, **kwargs)

    # pylint: disable=invalid-name, unused-variable
    def owlReceived(self, address, msg):
        ip, port = address

        if ip != self.src:
            # drop out, bad source
            raise ValueError('Source address does not match for packet')

        assert isinstance(msg, OwlElectricity), (
            'This only supports electricity messages.')

        # we are good.
        print(msg)

        # iterate channels sorted by channel name, and get their data
        chan_names = msg.channels.keys()
        chan_names.sort()

        ordered_channels = ['N']
        for channel in chan_names:
            ordered_channels.append(
                str(msg.channels[channel].current_w.to_integral_value()))
            ordered_channels.append(
                str(msg.channels[channel].daily_wh.to_integral_value()))

        ordered_channels = ':'.join(ordered_channels)

        # update database
        res = rrdtool.update(self.rrd, ordered_channels)

        if res:
            print(rrdtool.error())


if __name__ == '__main__':
    # pylint: disable=invalid-name
    parser = ArgumentParser()

    parser.add_argument('-s', '--src', dest='src',
                        help='Source address to accept data from. \
                              This is the IP of your OWL Intuition.')

    parser.add_argument('-i', '--iface', dest='iface', default='',
                        help='Network interface to use for getting data.')

    parser.add_argument('-r', '--rrd', dest='rrd', help='Path to RRD database')

    # pylint: disable=invalid-name
    options = parser.parse_args()
    # pylint: disable=invalid-name
    protocol = RrdOwlProtocol(src=options.src,
                              rrd=options.rrd,
                              iface=options.iface)
    # pylint: disable=no-member
    reactor.listenMulticast(MCAST_PORT, protocol, listenMultiple=True)
    reactor.run()
