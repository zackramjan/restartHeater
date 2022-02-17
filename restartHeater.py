#!/usr/bin/env python3
import json
import sys
import time
import traceback
from os import environ
from datetime import date, datetime


import requests
from pyHS100 import SmartPlug, SmartBulb
def logIt(msg):
    print(str(datetime.now()) + ": " + msg, file=sys.stderr, flush=True)

def main(argv=None): 
    heaterActivePower = 60
    powerStackSize = 30
    if "POWERDEPTH" in environ:
       powerStackSize = int(environ["POWERDEPTH"])

    powerStackMW = []
    for i in range(powerStackSize):
        powerStackMW.append(1)

    while True:
        try:
            plug = SmartPlug("192.168.1.83")
            e = plug.get_emeter_realtime()
            powerStackMW.append(round(e['power_mw']/1000))
            total = sum(powerStackMW)
            logIt("Current state: %s" % plug.state + " - Current consumption: %s" % e + " last: %s" % powerStackMW)
            powerStackMW.pop(0)
            if "ON" in plug.state and (total < heaterActivePower or (powerStackMW[-2] > heaterActivePower and powerStackMW[-1] + powerStackMW[-3] < heaterActivePower)):
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
                powerStackMW.append(1)
            powerStackMW.append(heaterActivePower)    

        time.sleep(60) 

if __name__ == '__main__':
    sys.exit(main())