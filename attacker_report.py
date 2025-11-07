#!/usr/bin/python   


# Name: London von Tungeln
# Date: 11/7/2025

import os
import subprocess
import re
import datetime
from geoip import geolite2

def main():
    os.system("clear")

    date = datetime.datetime.now().strftime("%B %d, %Y")
    print("Attacker Report - " + date)

if __name__ == "__main__":
    main()
