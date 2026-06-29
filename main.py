"""
Entry point
"""

import json

from menu import Menu
from models import CPU, Motherboard, GPU, PSU, RAM, CPUCooler, Case, Storage
from validator import PCBuild

def load_database(filename="database.json") -> dict:
    # Load JSON and convert raw dicts into class objects
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    # convert list of dicts into list of objects
    db = {
        "cpus": [CPU(**item) for item in data["cpus"]],
        "motherboards": [Motherboard(**item) for item in data["motherboards"]],
        "rams": [RAM(**item) for item in data["rams"]],
        "gpus": [GPU(**item) for item in data["gpus"]],
        "psus": [PSU(**item) for item in data["psus"]],
        "coolers": [CPUCooler(**item) for item in data["coolers"]],
        "cases": [Case(**item) for item in data["cases"]],
        "storages": [Storage(**item) for item in data["storages"]]
    }
    return db

def main():
    db = load_database()
    build = PCBuild() # Empty object of build
    menu = Menu(build=build, db=db)

    menu.start()

if __name__ == '__main__':
    main()
