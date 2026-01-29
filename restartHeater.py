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
    print(str(datetime.now())[0:16] + ": " + msg, file=sys.stderr, flush=True)

def main(argv=None): 
    heaterActivePower = 50
    MaxIntervalSinceLastRunMinutes = 60 
    snoozeIntervalMinutes = 5
    CheckPowerOn = False
    timeLastWorking =  time()
    snoozeStartTime =  time()
    powerT0 = 0
    powerT1 = 0
    powerT2 = 0
    
    if "POWERDEPTH" in environ:
       MaxIntervalSinceLastRunMinutes = int(environ["POWERDEPTH"])

    while True:
        try:
            
            plug = SmartPlug("192.168.1.83")
            if CheckPowerOn:
                plug.turn_on() 
                CheckPowerOn = False
          
            e = plug.get_emeter_realtime()
            logIt("%s" % plug.state + " { voltage_mv %s, " % e['voltage_mv'] + "power_mw %s }" % e['power_mw']) 

            powerT2 = powerT1
            powerT1 = powerT0
            powerT0 = round(e['power_mw']/1000)

            if powerT0+powerT1+powerT2 > heaterActivePower * 3:
                timeLastWorking =  time()

            if "ON" in plug.state and powerT0 < heaterActivePower and time() - timeLastWorking > MaxIntervalSinceLastRunMinutes * 60 and time() - snoozeStartTime > snoozeIntervalMinutes * 60:
                snoozeStartTime = time()
                logIt("turning OFF (timeout)")
                plug.turn_off()
                sleep(35)
                logIt("turning ON")
                plug.turn_on()
       
        except:
            CheckPowerOn = True
            traceback.print_exc()
              
        sleep(60) 

if __name__ == '__main__':
    sys.exit(main())