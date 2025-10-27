#!/usr/bin/python


# Name: London von Tungeln
# Date: 10/26/2025

import os
from pathlib import Path

DESKTOP = Path.home() / "Desktop"
HOME = Path.home()

def createSymbolicLink(): # symbolic link on desktop to ANY file
    
    
    source = Path(input("Enter the full path of the file to link: ").strip())

    if not source.exists():
        print(f"Error: file does not exist or cannot be found. Please try again.")
        return
    
    link_path = DESKTOP / source.name

    print(f"Source: '{source}'")
    print(f"Link path: '{link_path}'")
    print(f"Exists? {link_path.exists()}")

    if link_path.exists(): 
        print(f"Error: A file or link named '{source.name}' already exists on your desktop.")
        return
    
    try:
        os.symlink(source, link_path)
        print(f"Symbolic link created: '{link_path}'")
    except PermissionError:
        print(f"Error: Permission denied. Please run the script with sufficient privleges.")
    except Exception as e:
        print(f"Error: Unexpected Error: '{e}'")
    

def deleteSymbolicLink(): # delete symbolic link on desktop
    link_name = input("Enter the name of the symbolic link to delete (e.g., hello.txt): ").strip()
    link_path = DESKTOP / link_name

    if not link_path.exists() and not link_path.is_symlink():
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
    
    print("\n=== Symbolic Link Report===\n")
    symlinks_list = [] 

    for path in HOME.rglob("*"):
        if path.is_symlink():
            try:
                target = os.readlink(path)
            except OSError:
                target = "broken link"
            symlinks_list.append((path.relative_to(HOME), target))

    if not symlinks_list:
        print(f"No symbolic links found on your desktop.")
    else:
        print(f"Symbolic links found:")
        for link, target in symlinks_list:
            print(f"- {link} -> {target}")
    
    print(f"\n Total Symbolic links in home directory: {len(symlinks_list)}\n")
    print("=" * 40)

def main(): # clears terminal, handles UI
    os.system("clear")

    while True:
        print(f"\n=== Symbolic Link Manager ===")
        print(f"[1] Create Symbolic Link")
        print(f"[2] Delete Symbolic Link")
        print(f"[3] Generate a Symbolic Link Report")
        print(f"[4] Quit")

        choice = input("Select an option: ").strip()

        if choice == '1':
            createSymbolicLink()
        elif choice == '2':
            deleteSymbolicLink()
        elif choice == '3':
            generateReport()
        elif choice == '4' or choice.lower() == 'quit':
            print(f"Exiting...")
            break
        else:
            print(f"Invalid Option. Please choose 1-4")

if __name__ == "__main__":
    main()