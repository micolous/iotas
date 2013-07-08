# cdbusd module for iotas #

This is a module for working with Clipsal C-Bus in iotas.

It uses the [libcbus](https://github.com/micolous/cbus) Python modules and cdbusd (a PCI-sharing daemon that runs on D-Bus.

The module emulates some of the functionality of the Moore's Cloud Holiday API:

* Device.on
* Device.off
* Device.value
* Device.get_led_value
* Device.set_led_value

It takes in triplets for light values (like the Holiday) and then uses the highest value of the triplet to set the light level.  For example, if you passed (100, 150, 200), 200 would be your light value.

## Getting it running with a CBus PCI ##

In order to get the software running, you will first need to install [libcbus](https://github.com/micolous/cbus).  Once this is done, set up the DBus service with something like:

	$ cdbusd -S -s /dev/ttyUSB0

This will start up cdbusd using a serial PCI on `/dev/ttyUSB0`, using the session bus (`-S`) which is useful for testing or development.

You can also use TCP (network) PCIs with something like:

	$ cdbusd -S -t 192.168.1.40:22222
	
This will connect to a PCI on 192.168.1.40 port 22222.

Once this is done, setup the iotas with:

	app.licht = devices.cdbusd.driver.CDBusDriver(group_address=1, session_bus=True)

The group address given is the "default" which is used when emulating a simple switch.  You then run iotas.

You will then be able to pass commands to the C-Bus network with:

	>>> import requests, json
	>>> requests.put('http://127.0.0.1:8080/device/led/100/value', json.dumps(dict(value=[100, 100, 100])))

This will set group address 100 to the level 39.22% (`100 / 255`) instantly.

## Getting it running using a simulated PCI ##

As above, however use the following test program to emulate a TCP (network) PCI on 127.0.0.1:10001:

	$ python -m cbus.protocol.pciserverprotocol

You can then connect to the PCI in `cdbusd` with:

	$ cdbusd -S -t 127.0.0.1:10001

Then setup the connection in iotas with:

	app.licht = devices.cdbusd.driver.CDBusDriver(group_address=1, session_bus=True)

Then once iotas is started, you can send commands to your virtual PCI with:

	>>> import requests, json
	>>> requests.put('http://127.0.0.1:8080/device/led/100/value', json.dumps(dict(value=[100, 100, 100])))

And then the virtual PCI will report:

	2013-07-08 15:43:13+1000 [PCIServerProtocol,0,127.0.0.1] recv: '\\053800026464F9m'
	2013-07-08 15:43:13+1000 [PCIServerProtocol,0,127.0.0.1] recv: lighting ramp: 100, duration 0 seconds to level 39.22%
	2013-07-08 15:43:13+1000 [PCIServerProtocol,0,127.0.0.1] send: 'm.'

