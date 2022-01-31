#!/usr/bin/env python3
import json
import sys
import time
import traceback
from datetime import date, datetime


import requests
from pyHS100 import SmartPlug, SmartBulb
def logIt(msg):
    print(str(datetime.now()) + ": " + msg, file=sys.stderr, flush=True)

def main(argv=None): 
    heaterActivePower = 60000
    powerStackSize = 30
    powerStackMW = []
    for i in range(powerStackSize):
        powerStackMW.append(1400)

    while True:
        try:
            plug = SmartPlug("192.168.1.83")
            e = plug.get_emeter_realtime()
            powerStackMW.append(e['power_mw'])
            total = sum(powerStackMW)
            logIt("Current state: %s" % plug.state + " - Current consumption: %s" % plug.get_emeter_realtime() + " last: %s" % powerStackMW)
            powerStackMW.pop(0)
            if total < heaterActivePower and "ON" in plug.state:
                logIt("turning OFF")
                plug.turn_off()
                time.sleep(35)
                logIt("turning ON")
                plug.turn_on()
                powerStackMW.append(heaterActivePower)
                powerStackMW.pop(0)
        
        except:
            traceback.print_exc()
            powerStackMW = []
            for i in range(powerStackSize - 1):
                powerStackMW.append(1400)
            powerStackMW.append(heaterActivePower)    

        time.sleep(60) 

if __name__ == '__main__':
    sys.exit(main())