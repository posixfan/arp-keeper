# arp-keeper
Network scanning tool that can help you identify unknown devices on your network.

Author: Andrew Razuvaev <posixfan87@yandex.ru>

# How it works
It works by sender ARP 'who-has' requests for every IP address of the subnet. If the IP address is used by a device, it will reply with an ARP 'reply' packet. Each new device found is written to a database file. This way, you can take inventory of all the devices on your local network. Unknown devices may relate to an attacker.

# Install packages with pip and requirements.txt

The following command installs packages in bulk according to the configuration file, requirements.txt. In some environments, use pip3 instead of pip.
<pre>$ pip install -r requirements.txt</pre>

# New versions of Ubuntu and Debian use VENV
What is VENV => https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/

Quick Start Guide
<pre>
~/arp-keeper$ sudo apt install python3-venv
~/arp-keeper$ python3 -m venv venv
~/arp-keeper$ source venv/bin/activate
~/arp-keeper$ pip install -r requirements.txt
~/arp-keeper$ sudo .venv/bin/python3 arp-keeper.py eth0
</pre>
