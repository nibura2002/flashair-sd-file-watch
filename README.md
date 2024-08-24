# Watch Flashair file update via wifi in station mode
This is a playground for trying the feature of TOSHIBA Flash Air.
Simply get file list via cgi and download newly created file from specific directory.

- sample of CONFIG file in flashair
```
[Vendor]

CIPATH=/DCIM/100__TSB/FA000001.JPG
APPMODE=5
APPNAME=flashair
APPSSID={ssid}
APPNETWORKKEY={password}
VERSION={no-need-changing-from-default}
CID={no-need-changing-from-default}
PRODUCT=FlashAir
VENDOR=TOSHIBA
COMMANDCGI=100-221
```
- Note
1. Wi-fi will be stopped when file are not updated. Need to skip access error.