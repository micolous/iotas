#!/usr/bin/env python
import dbus


__all__ = [
	'CDBusDriver',
]

DBUS_INTERFACE = 'au.id.micolous.cbus.CBusInterface'
DBUS_SERVICE = 'au.id.micolous.cbus.CBusService'
DBUS_PATH = '/'


class CDBusApiFactory(object):
	api = {}
	
	def create_api(self, session_bus=False):
		# share api connections inside a single process so we don't run out of
		# fds to talk to dbus
		if session_bus not in self.api:		
			if session_bus:
				bus = dbus.SessionBus()
			else:
				bus = dbus.SystemBus()
			
			obj = bus.get_object(DBUS_SERVICE, DBUS_PATH)
			self.api[session_bus] = dbus.Interface(obj, DBUS_INTERFACE)

		return self.api[session_bus]


class CDBusDriver(object):
	def __init__(self, group_address, session_bus=False):
		self.group_address = group_address
		self._api = API_FACTORY.create_api(session_bus)


	def on(self):
		self._api.lighting_group_on(self.group_address)


	def off(self):
		self._api.lighting_group_off(self.group_address)
	
	def value(self):
		self._api.get_light_states(self.group_address)[0]


API_FACTORY = CDBusApiFactory()

