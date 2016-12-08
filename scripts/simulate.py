#!/usr/bin/env python

""" Simulate the solarcharger and vebus services so we can test this without
    having to buy an actual BMS. """

import dbus
import dbus.service
import dbus.mainloop.glib

import gobject

class BatteryService(dbus.service.Object):
    def __init__(self, path):
        self.count = 0
        bus_name = dbus.service.BusName("com.victronenergy.battery.socketcan_can0",
                dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, path)

    @dbus.service.method("com.victronenergy.BusItem", in_signature='', out_signature='i')
    def GetValue(self):
        self.count = (self.count + 1) % 2
        return self.count * 22
 
class DeviceService(dbus.service.Object):
    def __init__(self, name, path):
        bus_name = dbus.service.BusName(name, dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, path)
        self.path = path
        self.value = -1
        
    @dbus.service.method("com.victronenergy.BusItem", in_signature='i', out_signature='')
    def SetValue(self, v):
        print "{} set to {}".format(self.path, v)
        self.value = v

    @dbus.service.method("com.victronenergy.BusItem", in_signature='', out_signature='i')
    def GetValue(self):
        return self.value

if __name__ == "__main__":
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    s1 = BatteryService("/Info/MaxChargeCurrent")
    s2 = BatteryService("/Info/MaxDischargeCurrent")

    s3 = DeviceService("com.victronenergy.solarcharger.ttyUSB0", "/Link/NetworkMode")
    s4 = DeviceService("com.victronenergy.solarcharger.ttyUSB0", "/Link/ChargeCurrent")

    s5 = DeviceService("com.victronenergy.vebus.ttyUSB1", "/Mode")

    print "Running..."
    gobject.MainLoop().run()
