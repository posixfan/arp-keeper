# ARP Keeper

ARP Keeper is a Python script that scans your local network for new devices and keeps track of them in a CSV database. It can also send Telegram notifications when a new device is detected.

## Features

- **Network Scanning**: Scans the local network using ARP requests to detect connected devices.
- **Device Tracking**: Maintains a CSV database of known devices, including their MAC addresses, IP addresses, and manufacturers.
- **Telegram Notifications**: Optionally sends notifications to a Telegram chat when a new device is detected.
- **Cross-Platform**: Works on any system that supports Python 3 and Scapy.

## Installation

### Prerequisites

- Python 3.x
- `scapy` library
- `psutil` library
- `mac_vendor_lookup` library
- `requests` library

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/arp-keeper.git
   cd arp-keeper

2. **Install the required Python packages**:
   <pre>pip install -r requirements.txt</pre>

3. **Run the script**:
   <pre>sudo python3 arp-keeper.py interface [options]</pre>
   Replace <interface> with the name of your network interface (e.g., eth0, wlan0).

# New versions of Ubuntu and Debian use VENV
What is VENV => https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/

Quick Start Guide
<pre>
~/arp-keeper$ sudo apt install python3-venv
~/arp-keeper$ python3 -m venv venv
~/arp-keeper$ source venv/bin/activate
~/arp-keeper$ pip install -r requirements.txt
~/arp-keeper$ sudo .venv/bin/python3 arp-keeper.py interface
</pre>

# Usage
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

### Basic Usage
To start scanning your network, run the script with the network interface as an argument:
<pre>sudo python3 arp-keeper.py eth0</pre>

#### Options
- **--timeout**: Set the timeout between scans in seconds (default is 10 seconds).
  <pre>sudo python3 arp-keeper.py eth0 --timeout 15</pre>
- **--database**: Specify a custom path for the database file (default is database.csv).
  <pre>sudo python3 arp-keeper.py eth0 --database /path/to/database.csv</pre>
- **--telegram**: Enable Telegram notifications.
  <pre>sudo python3 arp-keeper.py eth0 --telegram</pre>

# Telegram notifications (--telegram)
To enable Telegram notifications, you need to set up a Telegram bot and obtain your API token and chat ID. Replace the placeholders in the send_telegram function with your actual API token and chat ID. \
\
![alt text](https://github.com/posixfan/arp-keeper/blob/main/img/telegram.png) \
\
How to create a telegram bot => https://t.me/BotFather \
The tool can work without Telegram. You decide whether to configure this option or not.

# Example Output
When a new device is detected, the script will print a message to the console and, if enabled, send a Telegram notification:
<pre>
  [!] New device detected
    MAC: 00:11:22:33:44:55
    IP: 192.168.1.100
    Manufacturer: Example Manufacturer
</pre>

The script will also display a table of known devices:
<pre>
----------------------------------------------------------------------------------------------------
|                                      Known devices                                               |
----------------------------------------------------------------------------------------------------
|      MAC address      |      IP address      |         Manufacturer         |     Description    |
----------------------------------------------------------------------------------------------------
|  00:11:22:33:44:55    |    192.168.1.100     | Example Manufacturer         |                    |
|  66:77:88:99:AA:BB    |    192.168.1.101     | Another Manufacturer         |                    |
----------------------------------------------------------------------------------------------------
</pre>

You can add a description for each device found in the "description" column of the database file.
![alt text](https://github.com/posixfan/arp-keeper/blob/main/img/Description.png) 

# Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

# Author
Andrew Razuvaev - [GitHub](https://github.com/posixfan) | [Email](posixfan87@yandex.ru)

# Acknowledgments
Thanks to the developers of **scapy**, **psutil**, **mac_vendor_lookup**, and requests for their excellent libraries.
