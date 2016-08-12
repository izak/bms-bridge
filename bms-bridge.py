#!/usr/bin/env python

import sys
from time import sleep
from argparse import ArgumentParser
import dbus

def find_services(bus, prefix):
    return [service for service in bus.list_names() \
        if service.startswith(prefix)]

def main():
    print("-------- bms bridge is starting up --------")
    parser = ArgumentParser(description='bms bridge')
    parser.add_argument('--session', action="store_true", help="Use session bus", default=False)
    parser.add_argument('--interval', type=int, help="Update MPPT this often, default 30 seconds", default=30)
    args = parser.parse_args()

    if args.session:
        bus = dbus.SessionBus()
    else:
        bus = dbus.SystemBus()

    # Find all solar chargers
    solarchargers = find_services(bus, 'com.victronenergy.solarcharger.')

    if not len(solarchargers):
        print >>sys.stderr, "No Solar Chargers found"
        sys.exit(2)

    while True: # or an exception kicks us out
        charge = bool(bus.get_object('com.victronenergy.battery.bmz',
            "/Info/MaxChargeCurrent").get_dbus_method('GetValue',
            "com.victronenergy.BusItem")())

        print("updating {} solarchargers. Charge is {}".format(len(solarchargers), charge))

        for s in solarchargers:
            ping = lambda: bus.get_object(s, '/Link/NetworkMode').get_dbus_method(
                'SetValue', 'com.victronenergy.BusItem')(9)
            update = bus.get_object(s, '/Link/ChargeCurrent').get_dbus_method(
                'SetValue', 'com.victronenergy.BusItem')
            ping()
            update(int(charge)*200)

        sleep(args.interval)

if __name__ == "__main__":
    main()
