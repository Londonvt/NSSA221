#!/usr/bin/python   


# Name: London von Tungeln
# Date: 10/3/2025

import os
import platform
import subprocess
import datetime
import socket

def run_command(cmd):
    return subprocess.getoutput(cmd).strip()

def get_mask():
    output = run_command("ip -f inet addr")
    for line in output.splitlines():
        line = line.strip()
        if line.startswith('inet'):
            ip_cidr =line.split()[1]
            ip, mask_length = ip_cidr.split("/")
            if not ip.startswith("127."):
                mask_length = int(mask_length)
                octets = []
                for _ in range(4):
                    if mask_length >= 8:
                        octets.append(255)
                        mask_length-= 8
                    else:
                        octets.append(sum(2**(7-i) for i in range(mask_length)))
                        mask_length = 0
                return ".".join(map(str,octets))

def system_report():

    date = datetime.datetime.now().strftime("%B %d, %Y")
    print("System Report - " + date + "\n")

    print("Device Information")
    fqdn = socket.getfqdn() #gives hostname and domain
    hostname = fqdn.split('.')[0]
    domain = ".".join(fqdn.split('.')[1:]) 
    print("Hostname: " + hostname)
    print("Domain: " + domain)

    #Network Information
    print("Network Information")
    print("Ip Address: " + run_command("hostname -I"))
    print("Gateway: " + run_command("ip route | grep default | awk '{print$3}'"))
    print("Subnet Mask: " + get_mask())
    print("DNS Servers: " + run_command("nmcli dev show | grep dns| awk '{print $2}'") )

    #Operating System Information

    #Storage Information

    #

def main():
    
    system_report()

main()