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




