IoTAS - the Internet of Things Access Server
--------------------------------------------

The Internet of Things Access Server is a universal, RESTful interface
for internet-of-things devices.

At the moment, the following devices are either partially or entirely implemented:

Holiday, Light and EngineRoom, all by MooresCloud

Hue by Philips

WeMo by Belkin

GPIOs by Linux (emphasis on Raspberry Pi)

There's a lot more to say and vastly more to document on all of this, 
but for the moment, it's important to give you just enough to invoke IoTAS
so that it can work in conjunction with the Holiday simulator.

Go into the IoTAS directory and invoke it as follows:

python iotas.py

IoTAS will try to use port 80 for its web access, but unless it's invoked as root 
(doable but not recommended at present), that will fail and it will fall back to port 8080.

IoTAS binds to network address 0.0.0.0, which means it will be visible on the opened port
at every network interface presented by the device (including localhost and 127.0.0.1)

At the present time, IoTAS provides copious output.  That will change.

Good luck!