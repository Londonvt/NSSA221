#!/usr/bin/python   


# Name: London von Tungeln
# Date: 11/7/2025

import os
import re
import datetime
from collections import defaultdict
import geoip2.database

LOG_FILE = "syslog.log"
THRESHOLD = 10
IP_PATTERN = re.compile(r'(\d+\.\d+\.\d+\.\d+)') 
FAIL_PATTERN = 'Failed password for root'
GEOIP_DB = "GeoLite2-Country.mmdb"


def parse_file():
    """Reads log files and outputs the ips that exceed failed login attempt limit"""
    attempts_count = defaultdict(int)

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

def get_country_code(ip, reader):

    """Takes IP and returns country code"""
    try:
        response = reader.country(ip)
        if response.country.iso_code:
            return response.country.iso_code
        return '??'
    except Exception as e:
        print(f"Error looking up ip {ip}: {e}")
        return "??"

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
    with geoip2.database.Reader(GEOIP_DB) as reader:
        for ip, count in sorted(
            suspicious_ips.items(),
            key=lambda item: item[1],   # sort by second element of tuple
            reverse=True                # highest to lowest
        ):
            country = get_country_code(ip, reader)
            print(f"{count:<6}{ip:<16}{country:<3}")



if __name__ == "__main__":
    main()
