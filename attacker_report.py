#!/usr/bin/python   


# Name: London von Tungeln
# Date: 11/7/2025

import os
import re
import datetime
from collections import defaultdict
from geoip import geolite2

GEOIP_DB = ""
LOG_FILE = "syslog.log"
THRESHOLD = 10

IP_PATTERN = re.compile(r'(\d+\.\d+\.\d+\.\d+)') 
FAIL_PATTERN = 'Failed password for root'

attempts_count = defaultdict(int)

def parse_file():
    """Reads log files and outputs the ips that exceed failed login attempt limit"""
    with open(LOG_FILE, "r") as log:
        for line in log:
            if FAIL_PATTERN in line:
                ip_match = IP_PATTERN.search(line)
                if ip_match:
                    ip = ip_match.group(1)
                    attempts_count[ip] += 1

    suspicious_ips = {}
    for ip, count in attempts_count.items():
        if count >= THRESHOLD:
            suspicious_ips[ip]=count

    return suspicious_ips

def get_country_code(ip):
    """Takes IP and returns country code"""
    match = geolite2.lookup(ip)
    print(f"DEBUG: IP={ip}, match={match}")  # <- debug line
    if match and match.country:
        return match.country
    return '??'

def main(): 
    """Clears terminal and handles output of code"""
    os.system("clear")
    date = datetime.datetime.now().strftime("%B %d, %Y")
    print("Attacker Report - " + date + "\n")
    
    suspicious_ips = parse_file()
    if not suspicious_ips:
        print("No suspicious IPs found.")
        return
    
    print(f"{'COUNT':<6}{'IP ADDRESS':<16}{'COUNTRY':<3}")
    for ip, count in sorted(
        suspicious_ips.items(),
        key=lambda item: item[1],   # sort by second element of tuple
        reverse=True                # highest to lowest
    ):
        country = get_country_code(ip)
        print(f"{count:<6}{ip:<16}{country:<3}")



if __name__ == "__main__":
    main()
