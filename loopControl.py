#!/usr/bin/env python

from jsonrpclib import Server

def main():
    api = Server("unix:/var/run/command-api.sock")
    logs = api.runCmds(1, ["show logging last 3 minutes"],"text" )
    loglines = logs[0]["output"].split('\n')
    loopedinterfaces= []
    for line in loglines:
        if "ETH-4-HOST_FLAPPING:" in line:
            linesplit = line.split(" ")
            for word in linesplit:
                if "Ethernet" in word or "Port-Channel" in word:
                    loopedinterfaces.append(word)
    commands = []
    for interface in loopedinterfaces:
        commands.append("errdisable test interface " + interface)
    if len(commands) > 0:
        api.runCmds(1, commands)
if __name__ == "__main__":
    main()

"""
event-handler loopcontrol
   action bash python /mnt/flash/loopControl.py
   delay 10
   !
   trigger on-logging
      regex EVPN-3-BLACKLISTED_DUPLICATE_MAC

management api http-commands
   protocol unix-socket
   no shutdown
"""