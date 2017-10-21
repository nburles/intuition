Protocol notes for Owl Intuition (Network Owl)
==============================================

Events are broadcast on LAN via Multicast UDP address ``224.192.32.19:22600``.  Events are transmitted in XML.

These events are from the OWL Intuition.
Official protocol documentation:

* `Multicast UDP (PDF)`_
* `API Documentation`_

.. _Multicast UDP (PDF): https://theowl.zendesk.com/hc/en-gb/article_attachments/200344663/Network_OWL_Multicast.pdf
.. _API Documentation: https://theowl.zendesk.com/hc/en-gb/articles/201284603-Multicast-UDP-API-Information

Note: Public protocol documentation does not reflect implementation in current firmware. There are minor changes 
to the content and structure of the XML messages.

.. highlight:: xml

electricity event
-----------------

These events are sent once every minute, and contain the live monitoring data from units connected to the Network Owl.

Example::

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

electricity.id
	MAC address of the device.
	
electricity.signal
	Metadata about the link quality between the sensor and the network reciever device.

electricity.battery
	Battery level in the sensor.

electricity.chan
	Channel information for each channel attached to the sensor.

solar event
-----------

Owl Intuition live solar monitoring data.

Example::

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

solar.id
	MAC address of device.

solar.current
	Current solar readings for generating and exporting.

solar.day
	Total for the day for electricty generated and exported.

hot water event
---------------

Live information from Owl Intuition hot water sensors.

Example:: 

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

hot_water.id
	MAC address of the device.

hot_water.zone
	Intuition supports up to 4 zones. Each zone contans temperature, battery and signal information.

hot_water.zone.temperature
	Contains the current hot water tank temperature (current), the required temperature (required) and the ambient temperature as the installed location.
	All temperatures are in degrees Celsius.

heating event
-------------

Live information from Owl Intuition heating sensors.

Example::
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

heating.id
	MAC address of the device.

heating.zone
	Intuition supports up to 4 zones. Each zone contans temperature, battery and signal information.

heating.zone.temperature
	Contains the current room/zone temperature (current) and the required temperature (required).	All temperatures are in degrees Celsius.

weather event
-------------

These show local weather information, not anything in the device.  It is retrieved from a web service that the Network Owl connects to.  There isn't any sensor in the Network Owl that gives this information.

Example::

	<weather id='443719123456' code='116'>
	  <temperature>11.00</temperature>
	  <text>Partly Cloudy</text>
	</weather>

weather.id
	MAC address of device.

weather.temperature
	Temperature, in degrees Celcius.

weather.text
	Description of local weather conditions.