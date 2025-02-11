# arp-keeper
Network scanning tool that can help you identify unknown devices on your network.

# How it works
It works by sender ARP 'who-has' requests for every IP address of the subnet. If the IP address is used by a device, it will reply with an ARP 'reply' packet. Each new device found is written to a database file. This way, you can take inventory of all the devices on your local network. Unknown devices may relate to an attacker.
