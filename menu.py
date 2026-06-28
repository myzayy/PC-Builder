"""
Menu: print and actions
"""

class Menu:
    def __init__(self, build, db):
        self.build = build
        self.db = db

    @staticmethod
    def show_menu(options: list, title: str):
        # Function to print components or actions
        print(f"\n==={title}===")
        for i, option in enumerate(options, 1):
            if hasattr(option, 'name'):
                print(f"{i}. {option.name} (${option.price})")
            else:
                print(f"{i}. {option}")
        print("\n0. Back / Exit")

    def print_current_build(self):
        build = self.build
        print("\n====================================")
        print("💻 PC Builder (CONSOLE VERSION)")
        print("====================================")
        print(f"Current build:")
        print(f"  • CPU: {build.cpu.name if build.cpu else 'Not selected'}")
        print(f"  • Motherboard: {build.motherboard.name if build.motherboard else 'Not selected'}")
        print(f"  • GPU: {build.gpu.name if build.gpu else 'Not selected'}")
        print(f"  • RAM: {str(build.ram_count) + "x " if build.ram_count else ""}"
              f"{build.ram.name if build.ram else 'Not selected'}")
        print(f"  • PSUS: {build.psu.name if build.psu else 'Not selected'}")
        print(f"  Total price: ${build.calculate_total_price()}")
        print("------------------------------------")

        print("1. Choose CPU")
        print("2. Choose Motherboard")
        print("3. Choose GPU")
        print("4. Choose RAM")
        print("5. Choose PSUS")
        print("6. Check compatibility")
        print("7. Save build to file")
        print("\n0. Exit")

    def get_user_choice(self, element: str, options_list: list):
        while True:
            print(f"Tip: Type 'del' or 'delete' to remove the current {element} from your build.")
            user_input = input("Your choice: ").strip().lower()
            if user_input == "0":
                return True
            if user_input in ["del", "delete"]:
                setattr(self.build, element, None)
                print(f"\n{element.capitalize()} has been removed from your build.")
                input("\nPress enter to continue...")
                return True
            try:
                idx = int(user_input) - 1
                if 0 <= idx < len(options_list):
                    setattr(self.build, element, options_list[idx])
                    return True
                else:
                    print("Error! Invalid component number.")
                    input("Press enter to continue...")
            except ValueError:
                print("Invalid input! Please enter a number.")
                input("Press enter to continue...")

    def handle_choice(self, choice):
        match choice:
            case "1":
                self.show_menu(self.db["cpus"], "CPU Choose")
                self.get_user_choice("cpu", self.db["cpus"])

            case "2":
                self.show_menu(self.db["motherboards"], "Motherboards Choose")
                self.get_user_choice("motherboard", self.db["motherboards"])
            case "3":
                self.show_menu(self.db["gpus"], "GPU Choose")
                self.get_user_choice("gpu", self.db["gpus"])
            case "4":
                self.show_menu(self.db["rams"], "RAM Choose")
                self.get_user_choice("ram", self.db["rams"])
                if self.build.ram:
                    while True:
                        ram_input = input("Choose ram count (1-4): ")
                        try:
                            count = int(ram_input)
                            if 1 <= count <= 4:
                                self.build.ram_count = count
                                break
                            else:
                                print("Error! You can only choose between 1 and 4 sticks.")
                        except ValueError:
                            print("Invalid input! Please enter a valid number.")
                else:
                    self.build.ram_count = None
            case "5":
                self.show_menu(self.db["psus"], "PSUS Choose")
                self.get_user_choice("psu", self.db["psus"])
            case "6":
                errors = self.build.check_compatibility()
                if not errors:
                    print("\nGreat choice! Your build fully compatible!")
                else:
                    print("\nCompatibility issues found:")
                    for error in errors:
                        print(error)
                input("\nPress Enter to continue...")
            case "7":
                if self.build.export_to_txt():
                    print("\n[SUCCESS] Your build has been successfully saved to .txt file.")
                    input("\nPress Enter to continue...")
                else:
                    print("\n[ERROR] Cannot export! Your build still has compatibility errors. Fix them first.")
                    input("\nPress Enter to continue...")
            case "0":
                print("\nGoodbye!")
                return False
            case _:
                print("Invalid choice! Please enter an option from 0 to 7.")
                input("\nPress Enter to continue...")
        return True

    def start(self):
        while True:
            self.print_current_build()
            choice = input("\nChoose option: ")
            if not self.handle_choice(choice):
                break
