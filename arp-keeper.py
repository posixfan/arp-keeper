#!/usr/bin/env python3
# https://github.com/posixfan/arp-keeper
import csv
import os
import psutil
from argparse import ArgumentParser
from ipaddress import IPv4Interface
from json import dumps
from requests import post
from socket import AF_INET
from time import sleep
from mac_vendor_lookup import MacLookup
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp

parser = ArgumentParser(description='Searches your local network for new devices.',
                        usage='arp-keeper.py iface [options]')
parser.add_argument('iface', type=str,
                    help='Name of the listening interface.')
parser.add_argument('--timeout', metavar='', type=int, default=10,
                    help='Timeout between LAN requests. The default is 15 seconds.')
parser.add_argument('--database', metavar='', type=str,
                    default='database.csv',
                    help='The path to the database file. '
                         'By default, a database.csv file is created.')
parser.add_argument('--telegram', action='store_true',
                    help='Send Telegram notifications')
args = parser.parse_args()

def is_running_as_root():
    return os.getuid() == 0

def is_file_writable(file_path):
    if not os.path.exists(file_path):
        choose = input(f'\033[33m[*]\033[0m The {file_path} file does not exist.\n'
                       f'    Create a new database file (y/n)? ')
        if choose != 'n':
            try:
                with open(file_path, 'a') as file:
                    pass
            except FileNotFoundError:
                print(f'\033[31m[-]\033[0m File path or access error: {file_path}')
                return False
        else:
            return False

    if not os.access(file_path, os.W_OK):
        print(f'\033[31m[-]\033[0m The {file_path} file is not writable.')
        return False

    print(f"\033[32m[+]\033[0m The {file_path} file exists and is writable.")
    return True

def get_subnet_address(interface_name):
    interfaces = psutil.net_if_addrs()

    if interface_name not in interfaces:
        raise ValueError(f'\033[31m[-]\033[0m The {interface_name} '
                         f'interface was not found')

    addresses = interfaces[interface_name]

    for addr in addresses:
        if addr.family == AF_INET:
            ip = IPv4Interface(f'{addr.address}/{addr.netmask}')
            return str(ip.network)

    raise ValueError(f'\033[31m[-]\033[0m No IPv4 address found on the '
                     f'{interface_name} interface')

def scan_network(subnet_address):
    arp = ARP(pdst=subnet_address)
    ether = Ether(dst='ff:ff:ff:ff:ff:ff')
    packet = ether/arp

    result = srp(packet, timeout=2, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

def get_manufacturer(mac_address):
    try:
        return MacLookup().lookup(mac_address)
    except:
        return f'Manufacturer not found'

def load_existing_devices(filename):
    if not os.path.exists(filename):
        return []

    devices = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            devices.append(row)
    return devices

def save_devices_to_file(filename, devices):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['mac', 'ip', 'manufacturer',
                                                  'description'])
        writer.writeheader()
        for device in devices:
            writer.writerow(device)

def send_telegram(line):
    api_token = ''
    CHAT_ID = '-'
    hook_url = f'https://api.telegram.org/bot{api_token}/sendMessage'
    msg_data = {}
    msg_data['chat_id'] = CHAT_ID
    msg_data['text'] = line
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    post(hook_url, headers=headers, data=dumps(msg_data, ensure_ascii=False))


def main():
    if not is_running_as_root():
        print('\033[31m[-]\033[0m Root rights are required')
        return

    if not is_file_writable(args.database):
        return

    try:
        interface_name = args.iface
        subnet_address = get_subnet_address(interface_name)
    except ValueError as e:
        print(e)
        return

    existing_devices = load_existing_devices(args.database)

    if existing_devices:
        print(f'{"-" * 100}\n'
              f'|{"Known devices".center(98)}|\n'
              f'{"-" * 100}\n'
              f'|{"MAC address".center(22)}|{"IP address".center(22)}|'
              f'{"Manufacturer".center(29)}|{"Description".center(22)}|\n'
              f'{"-" * 100}')
        for device in existing_devices:
            print(f'{device["mac"].center(23)}{device["ip"].center(24)}'
                  f'{device["manufacturer"].ljust(30)}{device["description"]}')
    else:
        print('\033[33m[*]\033[0m The file does not contain any known devices.')

    print()

    try:
        while True:
            print('\033[32m[+]\033[0m Network scanning...', end='\r')
            devices = scan_network(subnet_address)
            new_devices = []

            for device in devices:
                mac = device['mac']
                ip = device['ip']
                manufacturer = get_manufacturer(mac)

                if not any(d['mac'] == mac for d in existing_devices):
                    line = (f'New device detected\n'
                          f'    MAC: {mac}\n'
                          f'    IP: {ip}\n'
                          f'    Manufacturer: {manufacturer}')
                    print(f'\033[36m[!]\033[0m {line}\n')
                    new_devices.append({'mac': mac, 'ip': ip,
                                        'manufacturer': manufacturer})
                    if args.telegram:
                        send_telegram(line)

            if new_devices:
                existing_devices.extend(new_devices)
                save_devices_to_file(args.database, existing_devices)

            sleep(args.timeout)

    except KeyboardInterrupt:
        print('\n\033[33m[*]\033[0m The program is turned off')

if __name__ == '__main__':
    main()
