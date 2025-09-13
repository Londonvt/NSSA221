#!/usr/bin/python   

import subprocess
import os

def default_gateway():
    try:
        response = subprocess.check_output("ip route | grep default",shell=True,text=True)
        print("Default Gateway: ")
        print(response.strip())
        print("\n")
    except subprocess.CalledProcessError:
        print("Could not determine default gateway.\n")

def test_local_connectivity():
    print("Testing Local Connection (127.0.0.1)...\n")
    response = subprocess.run(["ping","-c","4","127.0.0.1"])
    if response.returncode == 0:
        print("Local Connectivity Test: SUCCESS")
    else:
        print("Local Connectivity Test: FAIL")

def test_remote_connectivity():
    print("Testing Remote Connection (129.21.3.17)...\n")
    response = subprocess.run(["ping","-c","4","129.21.3.17"])
    if response.returncode == 0:
        print("Remote Connectivity Test: SUCCESS")
    else:
        print("Remote Connectivity Test: FAIL")

def test_dns_resolution():
    print("Testing DNS Resolution (www.google.com)...\n")
    try:
        response = subprocess.check_output("dig +short www.google.com",shell=True,text=True)
        if response.strip():
            print("DNS Resolution Test: SUCCESS\n")
            print(response.strip)
        else:
            print("DNS Resolution Test: SUCCESS\n")
    except FileNotFoundError:
        print("File Not Found Error\n")

def main():
    while True:
        print("\n ---Network Test Menu---\n")
        print("1. Display the Default Gateway\n")
        print("2. Test Local Connectivity\n")
        print("3. Test Remote Connectivity\n")
        print("4. Test DNS Resolution\n")
        print("5. Exit/Quit the Script\n")

        choice = input("\n Enter your choice (1-5): ").strip()
        
        if choice == "1":
            default_gateway()
        elif choice == "2":
            test_local_connectivity()
        elif choice == "3":
            test_remote_connectivity()
        elif choice == "4":
            test_dns_resolution()
        elif choice == "5":
            print("Exiting Script\n")
            break
        else:
            print("Invalid Choice. Try Again.")
            
    

if __name__ == "__main__":
    main()