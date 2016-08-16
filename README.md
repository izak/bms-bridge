# BMS to VE-Direct bridge

This reads `/Info/MaxChargeCurrent` from the BMS and disables the charge
controllers if that value becomes zero.

Works only for VE.Direct MPPTs at the moment. It might be possible to
make it work for VE.Can MPPTs as well, since it is just an on/off 
function and we could use the /Mode switch for that.

Make sure to:
- have CCGX running at v1.70
- disable auto-update in CCGX, to prevent overwriting this custom work
- run the VE.Direct MPPT (one or multiple, all works) at v1.19

Checks to verify operation:
- The BmsPresent setting in the VE.Direct MPPTs should auto-change to Yes
- Unplugging the BMS from the CCGX should result in error 67 on the MPPT(s)
- Replugging back in should result in error disappearing, without requiring
  any reboots

## Installing the script
1) get yourself root access, and enable sshd
Explanations here: https://www.victronenergy.com/live/ccgx:root_access.
Note that it is not necessary to do the ssh-keys as explained on that page.

2) login to the ssh command line shell
See step 3 on the root_access page. As an end result you should see root@ccgx:~#,
which is the command prompt waiting for you to give it a command.

3) cut and paste these commands into the commandline:
```
cd /opt/color-control
wget https://github.com/mpvader/bms-bridge/archive/v1.2.tar.gz
tar -xzvf ./v1.2.tar.gz
mv ./bms-bridge-1.2 ./bms-bridge
ln -s /opt/color-control/bms-bridge/service /service/bms-bridge
```

Note that after pasting it starts immediately. And you might have to hit enter
one last time to execute the ln command.

What it does is, line by line:
```
rm: change directory
wget: download the version 1.2 of the script
tar: unzip it
mv: move it from /opt/color-control/bms-bridge-1.2 into /opt/color-control/bms-bridge
ln: add the service directory to the list of monitored and auto-started services.
```

Once done, the script will already be running in the background. And, since it is part of the
monitored services, it will be automatically restarted when it crashes. And started on bootup
of the device.

4) Diagnostics.
To see if it is running, do:
  svstat /service/bms-bridge

It will say how many seconds the service has been up.

And to see the logfiles, do: cat /log/bms-bridge/current | tai64nlocal

5) More info about commands
Enjoyed it and want to do more? See here:
https://www.victronenergy.com/live/open_source:ccgx:commandline
