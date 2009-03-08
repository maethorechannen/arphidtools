import dbus
import gobject

from dbus.mainloop.glib import DBusGMainLoop

def handle_arphid_attached_signal(arphid_id):
	print arphid_id

dbus_loop = DBusGMainLoop()

bus = dbus.SessionBus(mainloop=dbus_loop)
arphidd = bus.get_object("com.maethorechannen.arphidtools.Arphidd", "/com/maethorechannen/arphidtools/arphidd")
arphidd.connect_to_signal("ArphidAttachedSignal", handle_arphid_attached_signal)


loop = gobject.MainLoop()
loop.run()

