#!/usr/bin/env python

# Copyright (C) 2009 Scot McSweeney-Roberts <arphidtools _AT_ mcswenney-roberts.co.uk>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import dbus
import dbus.service
import gobject
import time

from dbus.mainloop.glib import DBusGMainLoop
from smartcard.System import readers

def get_direct_tx(command):
	return [0xFF, 0x00, 0x00, 0x00] + [len(command)] + command

def get_response(length):
	return [0xFF, 0xC0, 0x00, 0x00] + [length]

def get_led_control(led_state, control):
	return [0xFF, 0x00, 0x40] + [led_state] + [0x04] + control

def get_set_retry_time_to_one():
	return get_direct_tx([0xD4, 0x32, 0x05, 0x00, 0x00, 0x00])

def btos(b):
	return "%02X" % b

def concat(s1, s2):
	return s1 + s2

class Poller():
	def __init__(self, dbus_server):
		self.dbus_server = dbus_server
		r = readers()
		self.ttag = r[r.index('ACS ACR 38U-CCID 00 00')].createConnection()
		self.ttag.connect()
		#set retry time to 1
		RTO = get_set_retry_time_to_one()
		data, sw1, sw2 = self.ttag.transmit( RTO )

	def poll(self):
		POLL = [0xD4, 0x4A, 0x01, 0x00]
		while 1:
			time.sleep(1)
			data, sw1, sw2 = self.ttag.transmit( get_direct_tx(POLL) )
			if sw1 == 0x61:
				data, sw1, sw2 = self.ttag.transmit( get_response(sw2) )
				if data[2] == 0: #no tag found	
					#flash led and poll again
					print "no tag"
					#self.ttag.transmit(get_led_control(0x50, [0x05, 0x05, 0x03, 0x01]))
					self.ttag.transmit(get_led_control(0x50, [0x05, 0x05, 0x01, 0x01]))

				else:
					print data
					id_length = data[7]
					arphid_id = reduce(concat, map(btos,data[8:8+id_length]))
					self.dbus_server.ArphidReadSignal(arphid_id)

class Arphidd(dbus.service.Object):
	def __init__(self):
		object_path = '/com/maethorechannen/arphidtools/arphidd'
		dbus_interface='com.maethorechannen.arphidtools.Arphidd'
		bus_name = dbus.service.BusName(dbus_interface, bus=dbus.SessionBus())
		dbus.service.Object.__init__(self, bus_name, object_path)

	@dbus.service.signal('com.maethorechannen.arphidtools.Arphidd')
	def ArphidReadSignal(self, arphid_id):
		pass

if __name__ == '__main__':
	dbus_loop = DBusGMainLoop()
	bus = dbus.SessionBus(mainloop=dbus_loop)

	server = Arphidd()

	poller = Poller(server)
	poller.poll()
	loop = gobject.MainLoop()
	loop.run()

