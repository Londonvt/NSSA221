#!/usr/bin/python


# Name: London von Tungeln
# Date: 10/26/2025

import os
from pathlib import Path

DESKTOP = Path.home() / "Desktop"
HOME = Path.home()

def find_file(file_name):
    """Searches the entire filesystem for files with the given name."""

    matches = []
    for path in Path("/").rglob(file_name): 
        try:
            if path.is_file():
                matches.append(path)
        except PermissionError:
            continue
    return matches

def create_symbolic_link(): 
    """Creates a symbolic link on the Desktop for a specified file."""
    
    file_name = input(
        "Enter the name of the file to link (e.g, test.txt): "
    ).strip()
    matches = list(HOME.rglob(file_name))

    if not matches:
        print(f"Error: No file named '{file_name}' exists in any directory")
        return

    if len(matches) > 1:
        print(f"Multiple files named '{file_name}' found: ")    
        for index, path in enumerate(matches, 1):
            print(f"[{index}] {path}")
        choice = input("Enter the number for the file you want to link: ").strip()

        try:
            choice = int(choice)
            if not (1 <= choice <= len(matches)):
                print(f"Error: Invalid Choice.")
                return
        except ValueError:
            print(f"Error: Invalid Input.")
            return
        
        source = matches[choice - 1]
    else:
        source = matches[0]


    link_path = DESKTOP / source.name
    if link_path.exists(): 
        print(f"Error: A file or link named '{source.name}' already exists on your desktop.")
        return
    
    try:
        os.symlink(source, link_path)
        print(f"Symbolic link created: {link_path}")
    except PermissionError:
        print(
            "Error: Permission denied. Please run the script with sufficient privileges."
        )
    except Exception as e:
        print(f"Error: Unexpected Error: {e}")
    

def delete_symbolic_link(): 
    """Deletes a symbolic link on the Desktop by file_name."""

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
    

def generate_report(): 
    """Generate a report of all symbolic links in Home directory."""

    print("\n=== Symbolic Link Report===\n")
    symlinks = [] 

    for path in HOME.rglob("*"):
        if path.is_symlink():
            try:
                target = os.readlink(path)
            except OSError:
                target = "broken link"
            symlinks.append((path.relative_to(HOME), target))

    if not symlinks:
        print("No symbolic links found on your desktop.")
    else:
        print("Symbolic links found:")
        for link, target in symlinks:
            print(f"- {link} -> {target}")
    
    print(f"\nTotal Symbolic links in home directory: {len(symlinks)}\n")
    print("=" * 40)

def main(): 
    """
    Main menu for symbolic link manager.
    Clears the terminal, shows current working directory, and handles user input.
    """

    os.system("clear")
    print(f"Working Directory: {os.getcwd()}\n")

    while True:
        print("\n=== Symbolic Link Manager ===")
        print("[1] Create Symbolic Link")
        print("[2] Delete Symbolic Link")
        print("[3] Generate a Symbolic Link Report")
        print("[4] Quit")

        choice = input("Select an option: ").strip().lower()

        if choice == '1':
            create_symbolic_link()
        elif choice == '2':
            delete_symbolic_link()
        elif choice == '3':
            generate_report()
        elif choice in ("4", "quit"):
            print("Exiting...")
            break
        else:
            print("Invalid Option. Please choose 1-4")

if __name__ == "__main__":
    main()