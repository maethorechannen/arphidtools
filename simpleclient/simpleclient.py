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

"""
simpleclient.py

This is a simple client for the arphidd server. It listens for read events and prints the rfid id to stdout

"""
import dbus
import gobject

from dbus.mainloop.glib import DBusGMainLoop

def handle_arphid_read_signal(arphid_id):
	print arphid_id

if __name__ == '__main__':
	dbus_loop = DBusGMainLoop()

	bus = dbus.SessionBus(mainloop=dbus_loop)
	bus.add_signal_receiver(handle_arphid_read_signal,
                        dbus_interface="com.maethorechannen.arphidtools.Arphidd",
                        signal_name="ArphidReadSignal")
	loop = gobject.MainLoop()
	loop.run()

