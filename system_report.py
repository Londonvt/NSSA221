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

def get_mask(): #gets subnet mask
    output = run_command("ip -f inet addr") 
    for line in output.splitlines():
        line = line.strip()
        if line.startswith('inet'):
            ip_cidr =line.split()[1]
            ip, mask_length = ip_cidr.split("/") #gives subnetmask in /## format
            if not ip.startswith("127."): #skips localhost 
                mask_length = int(mask_length)
                octets = []
                for _ in range(4):
                    if mask_length >= 8: # if over 8, automatically sets octet to 255, decrements 8, and continues
                        octets.append(255)
                        mask_length-= 8
                    else:
                        octets.append(sum(2**(7-i) for i in range(mask_length))) # recursively does 2^7-i
                        mask_length = 0
                return ".".join(map(str,octets)) # converts int to str and joins strings into 1

def system_report():

    run_command("clear")

    date = datetime.datetime.now().strftime("%B %d, %Y")
    print("System Report - " + date + "\n")

    print("Device Information")
    fqdn = socket.getfqdn() #gives hostname and domain
    hostname = fqdn.split('.')[0]
    domain = ".".join(fqdn.split('.')[1:]) 
    print("Hostname: " + hostname)
    print("Domain: " + domain)

    #Network Information
    print("\nNetwork Information")
    print("Ip Address: " + run_command("hostname -I"))
    print("Gateway: " + run_command("ip route | grep default | awk '{print$3}'"))
    print("Subnet Mask: " + get_mask())
    print("DNS Servers: \n" + run_command("nmcli dev show | grep DNS| awk '{print $2}'") )

    #Operating System Information
    print("\nOperating System Information")

    raw_os_name = run_command("grep '^PRETTY_NAME=' /etc/os-release").strip()
    os_name = raw_os_name.split('=')[1].strip('"')
    
    raw_os_version = run_command("grep '^VERSION_ID=' /etc/os-release").strip()
    os_version = raw_os_version.split('=')[1].strip('"')

    print(f"Operating System: {os_name}")
    print(f"OS Version: {os_version}")
    print("Kernel Version: " + run_command("uname -r"))

    #Storage Information
    df_line = run_command("df -h /").splitlines()[1]
    parts = df_line.split()
    total, used, free = parts[1],parts[2],parts[3]

    print("\nStorage Information")

    print(f"System Drive Total: {total}")
    print(f"System Drive Used: {used}")
    print(f"System Drive Free: {free}")

    #CPU Information
    print("\nCPU Information")

    cores = run_command("grep 'physical id' /proc/cpuinfo | sort -u | wc -l") # counts all lines with physical id to find total 
    cpu_model = run_command("grep 'model name' /proc/cpuinfo").split(":")[1]
    processors = run_command("grep -c ^processor /proc/cpuinfo") #counts number of processors

    print(F"CPU Model: {cpu_model.strip()}" )
    print(F"Number of Processors: {processors}")
    print(F"Number of Cores: {cores}")

    #Ram Information
    print("\nRAM Information")

    total_ram = run_command("free -h | grep Mem: | awk '{print$2}'")
    available_ram = run_command("free -h | grep Mem: | awk '{print$7}'")

    print(F"Total Ram: {total_ram}")
    print(F"Available Ram: {available_ram}")


def main():
    
    system_report()

main()