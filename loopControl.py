#!/usr/bin/env python
from jsonrpclib import Server
import time

def main():
    api = Server("unix:/var/run/command-api.sock")
    logs = api.runCmds(1, ["show logging last 1 minutes"],"text" )
    loglines = logs[0]["output"].split('\n')
    excludedinterfaces = ["Cpu","Vxlan1","Port-Channel100"]
    loopedinterfaces = []
    for line in loglines:
        if "ETH-4-HOST_FLAPPING:" in line:
            linesplit = line.split(" ")
            for word in linesplit:
                if ("Ethernet" in word or "Port-Channel" in word) and (word not in excludedinterfaces):
                    loopedinterfaces.append(word)

    for interface in loopedinterfaces:
        intcountersfirst = api.runCmds(1, ["show interfaces counters"],"json" )[0]["interfaces"]
        time.sleep(10)
        intcounterssecond = api.runCmds(1, ["show interfaces counters"],"json" )[0]["interfaces"]
        if intcounterssecond[interface]["inBroadcastPkts"] - intcountersfirst[interface]["inBroadcastPkts"] > 10000:
            api.runCmds(1, ["errdisable test interface " + interface],"json" )
            api.runCmds(1,["send log message "+ interface+ " ERRDISABLED BY SCRIPT BECAUSE OF LOOP"])

if __name__ == "__main__":
    main()

"""
management api http-commands
   protocol unix-socket
   no shutdown

event-handler loopcontrolvlan
   action bash python /mnt/flash/loopControl.py
   repeat interval 60
   threshold 60 count 5
   !
   trigger on-logging
      regex ETH-4-HOST_(FLAPPING)
"""
