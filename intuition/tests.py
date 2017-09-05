#!/usr/bin/env python
"""
intuition/tests.py - Tests for Network Owl protocol parser
Copyright 2017 Martin Rowan
Copyright 2013-2014 Michael Farrell <micolous+git@gmail.com>

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
from decimal import Decimal
from .protocol import parse_datagram, OwlElectricity, OwlHeating, OwlChannel, OwlSolar, OwlWeather, OwlHotWater


def test_electricity():
    packet = """\
<electricity id='443719123456' ver='2.0'>
    <timestamp>1504296371</timestamp>
    <signal rssi='-42' lqi='15'/>
    <battery level='100%'/>
    <channels>
        <chan id='0'>
            <curr units='w'>257.00</curr>
            <day units='wh'>17.13</day>
        </chan>
        <chan id='1'>
            <curr units='w'>96.00</curr>
            <day units='wh'>6.40</day>
        </chan>
        <chan id='2'>
            <curr units='w'>32.00</curr>
            <day units='wh'>2.13</day>
        </chan>
        <chan id='3'>
            <curr units='w'>1175.00</curr>
            <day units='wh'>38966.80</day>
        </chan>
        <chan id='4'>
            <curr units='w'>1046.00</curr>
            <day units='wh'>12345.67</day>
        </chan>
        <chan id='5'>
            <curr units='w'>19.15</curr>
            <day units='wh'>534.89</day>
        </chan>
    </channels>
    <property>
        <current>
            <watts>1110.00</watts>
            <cost>10.62</cost>
        </current>
        <day>
            <wh>25026.31</wh>
            <cost>196.78</cost>
        </day>
        <tariff>
            <curr_price>0.10</curr_price>
            <block_limit>4294967295</block_limit>
            <block_usage>13523</block_usage>
        </tariff>
    </property>
</electricity>
"""

    msg = intuition.protocol.parse_datagram(packet)

    assert msg.mac == '443719123456'
    assert msg.rssi == -42
    assert msg.lqi == 15
    assert len(msg.channels) == 6
    assert msg.battery == 100
    
    for k, v in msg.channels.items():
        assert msg.channels[k].channel_id == k
        assert isinstance(msg.channels[k].current_w, Decimal)
        assert isinstance(msg.channels[k].daily_wh, Decimal)
        str(msg.channels[k])

    assert msg.channels['0'].current_w == Decimal('257.00')
    assert msg.channels['0'].daily_wh == Decimal('17.13')
    assert msg.channels['1'].current_w == Decimal('96.00')
    assert msg.channels['1'].daily_wh == Decimal('6.40')
    assert msg.channels['2'].current_w == Decimal('32.00')
    assert msg.channels['2'].daily_wh == Decimal('2.13')
    assert msg.channels['3'].current_w == Decimal('1175.00')
    assert msg.channels['3'].daily_wh == Decimal('38966.80')
    assert msg.channels['4'].current_w == Decimal('1046.00')
    assert msg.channels['4'].daily_wh == Decimal('12345.67')
    assert msg.channels['5'].current_w == Decimal('19.15')
    assert msg.channels['5'].daily_wh == Decimal('534.89')
    str(msg)

# def test_heating_22():
#     # from official protocol documentation
#     packet = """\
# <heating id='00A0C914C851'>
#     <signal rssi='-61' lqi='48'/>
#     <battery level='2730mV'/>
#     <temperature until='1359183600' zone='0'>
#         <current>22.37</current>
#         <required>15.00</required>
#     </temperature>
# </heating>
# """
    
#     msg = parse_datagram(packet)
    
#     assert msg.mac == '00A0C914C851'
#     assert msg.rssi == -61
#     assert msg.lqi == 48
#     assert len(msg.zones) == 1
    
#     assert msg.zones['0'].zone_id == '0'
#     assert msg.zones['0'].current_temp == Decimal('22.37')
#     assert msg.zones['0'].required_temp == Decimal('15.00')
#     str(msg)
#     str(msg.zones['0'])

def test_heating_23():
    # from official protocol documents for owl v2.3 and above
    packet = """\
<heating ver='2' id='00A0C914C851'>
    <timestamp>1384249792</timestamp>
    <zones>
        <zone id='200027F' last='26'>
            <signal rssi='-87' lqi='48'/>
            <battery level='2240'/>
            <conf flags='0'/>
            <temperature state='0' flags='0' until='1384273800' zone='0'>
                <current>21.30</current>
                <required>15.00</required>
            </temperature>
        </zone>
        <zone id='2000014' last='48'>
            <signal rssi='-58' lqi='48'/>
            <battery level='2960'/>
            <conf flags='0'/>
            <temperature state='0' flags='0' until='1384273800' zone='0'>
                <current>21.87</current>
                <required>15.00</required>
            </temperature>
        </zone>
    </zones>
</heating>
"""
    msg = parse_datagram(packet)

    assert msg.mac == '00A0C914C851'
    assert len(msg.zones) == 2
    assert msg.zones[0].zone_id == '200027F'
    assert msg.zones[0].rssi == '-87'
    assert msg.zones[0].lqi == '48'
    assert msg.zones[0].battery == '2240'
    assert msg.zones[0].current_temp == Decimal('21.30')
    assert msg.zones[0].required_temp == Decimal('15.00')
    assert msg.zones[1].zone_id == '2000014'
    assert msg.zones[1].rssi == '-58'
    assert msg.zones[1].lqi == '48'
    assert msg.zones[1].battery == '2960'
    assert msg.zones[1].current_temp == Decimal('21.87')
    assert msg.zones[1].required_temp == Decimal('15.00')
    str(msg)

def test_hotwater_23():
    packet = """\
<hot_water ver='2' id='00A0C914C851'>
    <timestamp>1384249810</timestamp>
    <zones>
        <zone id='200062E' last='2'>
            <signal rssi='-41' lqi='48'/>
            <battery level='2990'/>
            <conf flags='0'/>
            <temperature state='0' flags='0' until='1384725600'>
                <current>21.00</current>
                <required>45.00</required>
                <ambient>21.96</ambient>
            </temperature>
            <humidity>66.13</humidity>
        </zone>   
        <zone id='200062F' last='8'>
            <signal rssi='-45' lqi='43'/>
            <battery level='2990'/>
            <conf flags='0'/>
            <temperature state='0' flags='4097' until='1384725600'>
                <current>20.50</current>
                <required>50.00</required>
                <ambient>22.84</ambient>
            </temperature>
            <humidity>53.45</humidity>
        </zone>
    </zones>
</hot_water>
"""
    msg = parse_datagram(packet)

    assert msg.mac == '00A0C914C851'
    assert len(msg.zones) == 2
    assert msg.zones[0].zone_id == '200062E'
    assert msg.zones[0].rssi == '-41'
    assert msg.zones[0].lqi == '48'
    assert msg.zones[0].battery == '2990'
    assert msg.zones[0].current_temp == Decimal('21.00')
    assert msg.zones[0].required_temp == Decimal('45.00')
    assert msg.zones[0].ambient_temp == Decimal('21.96')
    assert msg.zones[0].humidity == Decimal('66.13')
    assert msg.zones[1].zone_id == '200062F'
    assert msg.zones[1].rssi == '-45'
    assert msg.zones[1].lqi == '43'
    assert msg.zones[1].battery == '2990'
    assert msg.zones[1].current_temp == Decimal('20.50')
    assert msg.zones[1].required_temp == Decimal('50.00')
    assert msg.zones[1].ambient_temp == Decimal('22.84')
    assert msg.zones[1].humidity == Decimal('53.45')

def test_solar():
    packet = """\
<solar id='443719100B48'>
    <timestamp>1504296372</timestamp>
    <current>
        <generating units='w'>2876.00</generating>
        <exporting units='w'>333.00</exporting>
    </current>
    <day>
        <generated units='wh'>21715.15</generated>
        <exported units='wh'>10388.81</exported>
    </day>
</solar>
"""
    msg = parse_datagram(packet)
    assert msg.mac == '443719100B48'
    # TODO ADD TESTS
    assert msg.generating.current_w == Decimal('2876.00')
    assert msg.generating.daily_wh == Decimal('21715.15')
    assert msg.exporting.current_w == Decimal('333.00')
    assert msg.exporting.daily_wh == Decimal('10388.81')
    str(msg)

def test_weather():
    packet="""\
<weather id='00A0C914C851' code='113'>
    <temperature>15.00</temperature>
    <text>Clear/Sunny</text>
</weather>
"""
    msg = parse_datagram(packet)
    assert msg.mac == '00A0C914C851'
    assert msg.temperature == Decimal('15.00')
    assert msg.text == 'Clear/Sunny'
    str(msg)