# loopControl

EVPN has a built-in mechanism where if by default there are minimum 5 MAC moves in 180 seconds, it prevents this MAC to be advertised to its peers. However this does not stop the data plane loops. The intention of this script is to errdisable the interfaces that MAC move is seen, thus break the data plane loop.

This script is triggered in event-handler when EVPN-3-BLACKLISTED_DUPLICATE_MAC message is seen in the logs. The script parses the log messages seen in the last 180 seconds to catch ETH-4-HOST_FLAPPING and errdisables Ethernet and Port-Channel interfaces. Make sure to exclude peer-link interfaces if there are any.
