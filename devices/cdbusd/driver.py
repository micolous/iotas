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
		"""
		:param group_address: Default group address to control on the CBus.  Used by :meth:`on` and :meth:`off`.
		:type group_address: int
		
		:param session_bus: In development mode, cdbusd uses the Session Bus instead of the System Bus.  When set to True, this uses the Session Bus instead of the System Bus.
		:type session_bus: bool
		
		"""
		self.group_address = group_address
		self._api = API_FACTORY.create_api(session_bus)


	def on(self):
		self._api.lighting_group_on([self.group_address])


	def off(self):
		self._api.lighting_group_off([self.group_address])


	def value(self):
		return self.get_led_value(self.group_address)
		
	
	def set_led_value(self, group_address, triplet):
		# we don't actually care what is in the triplet, we just implement it
		# "like" the holiday by taking the highest value in the triplet as our
		# level.
		
		# level values are 0..255, convert to float
		level = max(triplet) / 255.
		
		assert 0. <= level <= 1., 'Light level must be 0..255.'
		
		# 0 == duration of fade.  run instantly.
		self._api.lighting_group_ramp(group_address, 0, level)


	def get_led_value(self, group_address):
		return int(self._api.get_light_states([group_address])[0] * 255.)
		
		


API_FACTORY = CDBusApiFactory()

