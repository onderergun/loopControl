# loopControl

EVPN has a built-in mechanism where if by default there are minimum 5 MAC moves in 180 seconds, it prevents this MAC to be advertised to its peers. However this does not stop the data plane loops. The intention of this script is to errdisable the interfaces that MAC move is seen, thus break the data plane loop.

This script is triggered in event-handler when the number of ETH-4-HOST_FLAPPING log messages exceed a certain user defined number in a time period. The script parses the log messages seen in the last 1 minute to get the Ethernet and Port-Channel interfaces. It only errdisables the interfaces that have > 10000 ingress broadcast packets in 10 seconds.

Make sure to exclude peer-link interfaces if there are any.
