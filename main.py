"""
Entry point
"""

from database import Database
from menu import Menu
from validator import PCBuild

def main():
    db = Database.load_database()

    build = PCBuild() # Empty object of build
    Menu(build=build, db=db).start()

if __name__ == '__main__':
    main()
