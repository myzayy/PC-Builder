"""
Entry point
"""

from database import Database
from menu import Menu
from validator import PCBuild

def main():
    db = Database.load_database()

    build = PCBuild() # Empty object of build
    menu = Menu(build=build, db=db)

    menu.start()

if __name__ == '__main__':
    main()
