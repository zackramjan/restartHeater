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
    powerStackMW = [0,0,0,0,0,0,10001]
    while True:
        try:
            plug = SmartPlug("192.168.1.83")
            e = plug.get_emeter_realtime()
            powerStackMW.append(e['power_mw'])
            total = sum(powerStackMW)
            logIt("Current state: %s" % plug.state + " - Current consumption: %s" % plug.get_emeter_realtime() + " last: %s" % powerStackMW)
            powerStackMW.pop(0)
            if total < 10000 and "ON" in plug.state:
                logIt("turning OFF")
                plug.turn_off()
                time.sleep(35)
                logIt("turning ON")
                plug.turn_on()
                powerStackMW.append(10001)
                powerStackMW.pop(0)
        
        except:
            traceback.print_exc()
        time.sleep(60) 

if __name__ == '__main__':
    sys.exit(main())