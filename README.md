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

# How to use it
<pre>
usage: arp-keeper.py iface [options]

Searches your local network for new devices.

positional arguments:
  iface        Name of the listening interface.

options:
  -h, --help   show this help message and exit
  --timeout    Timeout between LAN requests. The default is 15 seconds.
  --database   The path to the database file. By default, a database.csv file is created.
  --telegram   Send Telegram notifications
</pre>

# Telegram notifications (--telegram)
If you want to use the Telegram notification, you need to edit the 'api_token' and 'CHAT_ID' variables. (see the screenshot below). \
\
![alt text](https://github.com/posixfan/arp-keeper/blob/main/img/telegram.png) \
\
How to create a telegram bot => https://t.me/BotFather \
The tool can work without Telegram. You decide whether to configure this option or not.

# Launch example
The first launch. A database.csv database file is created where all found devices are recorded.
<pre>$ sudo ./arp-keeper.py eth0</pre>

Launch with a 30-second network polling timeout and a telegram notification.
<pre>$ ./arp-keeper.py eth0 --timeout 30 --telegram</pre>

You can add a description for each device found in the "description" column of the database file.
![alt text](https://github.com/posixfan/arp-keeper/blob/main/img/Description.png) 
