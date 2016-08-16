#!/usr/bin/python -u

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
    parser.add_argument('--interval', type=int, help="Update MPPT this often, default 5 seconds", default=5)
    args = parser.parse_args()

    if args.session:
        bus = dbus.SessionBus()
    else:
        bus = dbus.SystemBus()

    while True: # or an exception kicks us out
        # Find all solar chargers
        solarchargers = find_services(bus, 'com.victronenergy.solarcharger.')

        # When com.victronenergy.battery.bmz service is not available, for
        # whichever reason, the script will crash and relies on daemontools to 
        # restart it. Result is that the solar charger will automatically stop 
        # charging since it doesn't receive the pings anymore. And it will raise
        # error 67: Missing the BMS. 
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
