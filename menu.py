"""
Menu: print and actions
"""
import os

class Menu:
    def __init__(self, build, db):
        self.build = build
        self.db = db
        self.component_map = {
            "1": ("cpu", "cpus", "CPU Selection"),
            "2": ("motherboard", "motherboards", "Motherboard Selection"),
            "3": ("gpu", "gpus", "Gpu Selection"),
            # RAM logic separated because of choose count logic
            "5": ("psu", "psus", "Power Supply Selection"),
            "6": ("storage", "storages", "Storage Selection"),
            "7": ("cpu_cooler", "coolers", "CPU Cooler Selection"),
            "8": ("case", "cases", "Case Selection")
        }
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def show_menu(options: list, title: str):
        # Function to print components or actions
        Menu.clear_screen()
        print(f"\n==={title}===")
        for i, option in enumerate(options, 1):
            if hasattr(option, 'name'):
                print(f"{i}. {option.name} (${option.price})")
            else:
                print(f"{i}. {option}")
        print("\n0. Back / Exit")

    def print_current_build(self):
        Menu.clear_screen()
        build = self.build
        print("\n====================================")
        print("💻 PC Builder (CONSOLE VERSION)")
        print("====================================")
        print(f"Current build:")
        print(f"  • CPU: {build.cpu.name if build.cpu else 'Not selected'}")
        print(f"  • Motherboard: {build.motherboard.name if build.motherboard else 'Not selected'}")
        print(f"  • GPU: {build.gpu.name if build.gpu else 'Not selected'}")

        ram_prefix = f"{build.ram_count}x " if build.ram_count else ""
        print(f"  • RAM: {ram_prefix}{build.ram.name if build.ram else 'Not selected'}")

        print(f"  • PSUS: {build.psu.name if build.psu else 'Not selected'}")
        print(f"  • Storage: {build.storage.name if build.storage else 'Not selected'}")
        print(f"  • CPU Cooler: {build.cpu_cooler.name if build.cpu_cooler else 'Not selected'}")
        print(f"  • Case: {build.case.name if build.case else 'Not selected'}")
        print(f"  Total price: ${build.calculate_total_price()}")
        print("------------------------------------")

        print("1. Choose CPU \n2. Choose Motherboard \n3. Choose GPU \n4. Choose RAM \n5. Choose PSUS \n"
              "6. Choose Storage \n7. Choose CPU Cooler \n8. Choose Case ")

        print("------------------------------------")
        print("9. Check compatibility \n10. Save build to file \n")
        print("0.Exit")

    def get_user_choice(self, element: str, options_list: list):
        while True:
            print(f"\nTip: Type 'del' or 'delete' to remove the current {element} from your build.")
            user_input = input("Your choice: ").strip().lower()
            if user_input == "0":
                return True
            if user_input in ["del", "delete"]:
                setattr(self.build, element, None)
                print(f"\n[INFO] {element.replace('_', ' ').capitalize()} has been removed.")
                input("\nPress Enter to continue...")
                return True
            try:
                idx = int(user_input) - 1
                if 0 <= idx < len(options_list):
                    setattr(self.build, element, options_list[idx])
                    return True
                print("❌ Error! Invalid component number.")
            except ValueError:
                print("⚠️ Invalid input! Please enter a number.")
            input("Press Enter to continue...")

    def handle_choice(self, choice):

        if choice in self.component_map:
            attr_name, db_key, title = self.component_map[choice]
            self.show_menu(self.db[db_key], title)
            self.get_user_choice(attr_name, self.db[db_key])
            return True

        match choice:
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
                                print("⚠️ Error! You can only choose between 1 and 4 sticks.")
                        except ValueError:
                            print("⚠️ Invalid input! Please enter a valid number.")
                        input("Press Enter to continue")
                else:
                    self.build.ram_count = None

            case "9":
                errors = self.build.check_compatibility()
                if not errors:
                    print("\n✅ Great choice! Your build fully compatible!")
                else:
                    print("\n⚠️ Compatibility issues found:")
                    for error in errors:
                        print(f"  ❌ {error}")
                input("\nPress Enter to continue...")
            case "10":
                if self.build.export_to_txt():
                    print("\n💾 [SUCCESS] Your build has been successfully saved to .txt file.")
                    input("\nPress Enter to continue...")
                else:
                    print("\n❌ [ERROR] Cannot export! Your build still has compatibility errors. Fix them first.")
                    input("\nPress Enter to continue...")
            case "0":
                print("\n👋 Goodbye!")
                return False
            case _:
                print("⚠️ Invalid choice! Please enter an option from 0 to 10.")
                input("\nPress Enter to continue...")
        return True

    def start(self):
        while True:
            self.print_current_build()
            choice = input("\nChoose option: ")
            if not self.handle_choice(choice):
                break
