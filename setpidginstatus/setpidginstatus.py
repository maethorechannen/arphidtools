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
import gobject

from dbus.mainloop.glib import DBusGMainLoop


#some constants from http://developer.pidgin.im/wiki/DbusHowto
STATUS_OFFLINE = 1
STATUS_AVAILABLE = 2
STATUS_UNAVAILABLE = 3
STATUS_INVISIBLE = 4
STATUS_AWAY = 5
STATUS_EXTENDED_AWAY = 6
STATUS_MOBILE = 7
STATUS_TUNE = 8

statii = {
	"04C8FFB9212580": STATUS_AVAILABLE,
	"045309B9212584": STATUS_AWAY
}

if __name__ == '__main__':
	dbus_loop = DBusGMainLoop()

	bus = dbus.SessionBus(mainloop=dbus_loop)

	obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
	purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")
	
	def handle_arphid_read_signal(arphid_id):
		active_accounts = purple.PurpleAccountsGetAllActive()
		for active_account in active_accounts:
			presence = purple.PurpleAccountGetPresence(active_account)
			status_id = purple.PurplePrimitiveGetIdFromType(statii[arphid_id])
			purple.PurplePresenceSwitchStatus(presence,status_id)			

	arphidd = bus.get_object("com.maethorechannen.arphidtools.Arphidd", "/com/maethorechannen/arphidtools/arphidd")
	arphidd.connect_to_signal("ArphidReadSignal", handle_arphid_read_signal)

	loop = gobject.MainLoop()
	loop.run()

