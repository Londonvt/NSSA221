#!/usr/bin/python   


# Name: London von Tungeln
# Date: 10/26/2025

import subprocess
import os
from pathlib import Path

DESKTOP = Path.home() / "Desktop"
HOME = Path.home()

def createSymbolicLink(): # symbolic link on desktop to ANY file
    
    
    source = Path(input("Enter the full path of the file to link: ").strip())

    if not source.exists():
        print("Error: file does not exist or cannot be found. Please try again.")
        return
    
    link_path = DESKTOP / source.name

    if link_path.exists: 
        print(f"Error: A file or link named '{source.name}' already exists on your desktop.")
        return
    
    try:
        os.symlink(source, link_path)
        print(f"Symbolic link created: '{link_path}")
    except PermissionError:
        print("Error: Permission denied. Please run the script with sufficient privleges.")
    except Exception as e:
        print(f"Error: Unexpected Error: '{e}'")
    

def deleteSymbolicLink(): # delete symbolic link on desktop
    link_name = input("Enter the name of the symbolic link to delete (e.g., hello.txt): ").strip()
    link_path = DESKTOP / link_name

    if not link_path.exists and not link_path.is_symlink():
        print(f"Error: '{link_name}' does not exist on your desktop.")
        return
    
    if not link_path.is_symlink():
        print(f"Error: '{link_name}' is not a symbolic link.")
        return
    
    try:
        link_path.unlink()
        print(f"Symbolic link '{link_name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting symbolic link: {e}")
    

def generateReport(): #lists all symbolic links on desktop, their target paths, and count of links in the user's home directory
    symlinks = [f for f in DESKTOP.iterdir() if f.is_symlink] # Array of symlinks

    print("\n === Symbolic Link Report ===")
    if not symlinks:
        print("No symbolic links found on your desktop.")
    else:
        for link in symlinks:
            target = os.readlink(link)
            print(f"{link.name} -> {target}")
    total_links = sum(1 for f in HOME.rglob("*") if f.is_symlink())
    print(f"\n Total Symbolic links in home directory: {total_links}")

def main(): # clears terminal, handles UI
    os.system("clear")

    while True:
        print("\n=== Symbolic Link Manager ===")
        print("[1] Create Symbolic Link")
        print("[2] Delete Symbolic Link")
        print("[3] Generate a Symbolic Link Report")
        print("[4] Quit")

        choice = input("Select an option: ").strip()

        if choice == '1':
            createSymbolicLink()
        if choice == '2':
            deleteSymbolicLink()
        if choice == '3':
            generateReport()
        if choice == '4' or choice.lower() == 'quit':
            print("Exiting")
            break
        else:
            print("Invalid Option. Please choose 1-4")

if __name__ == "__main__":
    main()