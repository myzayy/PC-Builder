'''
Entry point
'''

import json

from models import CPU, Motherboard, GPU, PSU, RAM
from validator import PCBuild

def load_database(filename="database.json") -> dict:
    # Load json and convert raw dicts into class objects
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    # convert list of dicts into list of objects
    db = {
        "cpus": [CPU(**item) for item in data["cpus"]],
        "motherboards": [Motherboard(**item) for item in data["motherboards"]],
        "rams": [RAM(**item) for item in data["rams"]],
        "gpus": [GPU(**item) for item in data["gpus"]],
        "psus": [PSU(**item) for item in data["psus"]]
    }
    return db

def show_menu(options: list, title: str):
    # Function to print components or actions
    print(f"\n==={title}===")
    for i, option in enumerate(options, 1):
        if hasattr(option, 'name'):
            print(f"{i}. {option.name} (${option.price})")
        else:
            print(f"{i}. {option}")
    print("\n0. Back / Exit")

def main():
    db = load_database()
    build = PCBuild() # Empty object of build

    while True:
        print("\n====================================")
        print("💻 PC Builder (CONSOLE VERSION)")
        print("====================================")
        print(f"Current build:")
        print(f"  • CPU: {build.cpu.name if build.cpu else 'Not selected'}")
        print(f"  • Motherboard: {build.motherboard.name if build.motherboard else 'Not selected'}")
        print(f"  • GPU: {build.gpu.name if build.gpu else 'Not selected'}")
        print(f"  • RAM: {str(build.ram_count) + "X \n\t\t\t" if build.ram_count else ""}"
              f"{build.ram.name if build.ram else 'Not selected'}")
        print(f"  • PSUS: {build.psu.name if build.psu else 'Not selected'}")
        print(f"  Total price: ${build.calculate_total_price()}")
        print("------------------------------------")

        print("1. Choose CPU")
        print("2. Choose Motherboard")
        print("3. Choose RAM")
        print("4. Choose GPU")
        print("5. Choose PSUS")
        print("6. Check compatibility")
        print("\n0. Exit")

        choice = input("\nChoose option: ")

        match choice:
            case "1":
                show_menu(db["cpus"], "CPU Choose")
                idx = int(input("Your choice: ")) - 1
                if 0 <= idx < len(db["cpus"]):
                    build.cpu = db["cpus"][idx] # write object in build

            case "2":
                show_menu(db["motherboards"], "Motherboards Choose")
                idx = int(input("Your choice: ")) - 1
                if 0 <= idx < len(db["motherboards"]):
                    build.motherboard = db["motherboards"][idx] # write object in build
            case "3":
                show_menu(db["rams"], "RAM Choose")
                idx = int(input("Your choice: ")) - 1
                if 0 <= idx < len(db["rams"]):
                    build.ram = db["rams"][idx]  # write object in build
                    build.ram_count = int(input("Choose ram count(Enter to keep 1): "))

            case "4":
                show_menu(db["gpus"], "GPU Choose")
                idx = int(input("Your choice: ")) - 1
                if 0 <= idx < len(db["gpus"]):
                    build.gpu = db["gpus"][idx]  # write object in build
            case "5":
                show_menu(db["psus"], "PSUS Choose")
                idx = int(input("Your choice: ")) - 1
                if 0 <= idx < len(db["psus"]):
                    build.psu = db["psus"][idx]  # write object in build
            case "6":
                errors = build.check_compatibility()
                if not errors:
                    print("\nGreat choice! Your build fully compatible!")
                else:
                    print("\nCompatibility issues found:")
                    for error in errors:
                        print(error)
                input("\nPress Enter to continue...")
            case "0":
                print("\nGoodbye!")
                break
            case _:
                print("Invalid choice! Please enter an option from 0 to 5.")
                input("\nPress Enter to continue...")

if __name__ == '__main__':
    main()
