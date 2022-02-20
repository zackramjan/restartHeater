#!/usr/bin/env python3
import json
import sys
from time import time, sleep
import traceback
from os import environ
from datetime import date, datetime


import requests
from pyHS100 import SmartPlug, SmartBulb
def logIt(msg):
    print(str(datetime.now()) + ": " + msg, file=sys.stderr, flush=True)

def main(argv=None): 
    heaterActivePower = 50
    powerStackSize = 30
    lastTimeCheck = 0;
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
            maxWattage = max(powerStackMW)
            logIt("Current state: %s" % plug.state + " - %s" % e + " last: %s" % powerStackMW)
            powerStackMW.pop(0)
            if "ON" in plug.state and maxWattage < heaterActivePower and time() - lastTimeCheck > powerStackSize * 60:
                lastTimeCheck = time()
                logIt("turning OFF (timeout)")
                plug.turn_off()
                sleep(35)
                logIt("turning ON")
                plug.turn_on()
            elif "ON" in plug.state and powerStackMW[-1] < heaterActivePower and powerStackMW[-2] > heaterActivePower and (powerStackMW[-3] < heaterActivePower or powerStackMW[-4] < heaterActivePower):
                logIt("turning OFF (short cycle)")
                plug.turn_off()
                sleep(35)
                logIt("turning ON")
                plug.turn_on()
       
        except:
            traceback.print_exc()
            powerStackMW = []
            lastTimeCheck = time()
            for i in range(powerStackSize - 1):
                powerStackMW.append(1)
              

        sleep(60) 

if __name__ == '__main__':
    sys.exit(main())