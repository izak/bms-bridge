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
    parser.add_argument('--bms', help="DBUS service name for the BMS", default="com.victronenergy.battery.socketcan_can0")
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

        # Find all vebus devices
        vebuses = find_services(bus, 'com.victronenergy.vebus.')

        # When bms service is not available, for whatever reason, the script
        # will crash and rely on daemontools to restart it. Result is that
        # the solar charger will automatically stop charging since it doesn't
        # receive the pings anymore. And it will raise error 67: Missing the
        # BMS. 
        charge = bool(bus.get_object(args.bms,
            "/Info/MaxChargeCurrent").get_dbus_method('GetValue',
            "com.victronenergy.BusItem")())

        discharge = bool(bus.get_object(args.bms,
            "/Info/MaxDischargeCurrent").get_dbus_method('GetValue',
            "com.victronenergy.BusItem")())

        print("updating {} solarchargers. Charge is {}".format(len(solarchargers), charge))

        for s in solarchargers:
            ping = lambda: bus.get_object(s, '/Link/NetworkMode').get_dbus_method(
                'SetValue', 'com.victronenergy.BusItem')(9)
            update = bus.get_object(s, '/Link/ChargeCurrent').get_dbus_method(
                'SetValue', 'com.victronenergy.BusItem')
            ping()
            update(int(charge)*200)

        print("updating {} vebus systems. Discharge is {}".format(len(vebuses), discharge))

        for v in vebuses:
            mode = int(bus.get_object(v, '/Mode').get_dbus_method(
                    'GetValue', 'com.victronenergy.BusItem')())

            # If off, leave it off.
            if mode == 4:
                print("{} is switched off, leaving it off".format(v))
                continue

            update = bus.get_object(v, '/Mode').get_dbus_method(
                'SetValue', 'com.victronenergy.BusItem')
            update(3 if discharge else 1)

        sleep(args.interval)

if __name__ == "__main__":
    main()
