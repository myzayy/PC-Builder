"""
Compatibility check logic
"""

class PCBuild:
    def __init__(self):
        self.cpu = None
        self.motherboard = None
        self.ram = None
        self.ram_count = None
        self.gpu = None
        self.psu = None

    def calculate_total_price(self) -> float:
        total_price = 0
        components = [self.cpu, self.motherboard, self.gpu, self.psu]
        for item in components:
            if item:
                total_price += float(item.price)

        if self.ram and self.ram_count:
            total_price += float(self.ram.price) * int(self.ram_count)

        return total_price

    def check_compatibility(self) -> list:
        errors = []
        required_components = {
            "Processor (CPU)": self.cpu,
            "Motherboard": self.motherboard,
            "RAM": self.ram,
            # "Graphics Card (GPU)": self.gpu,
            "Power Supply (PSU)": self.psu
        }

        for name, item in required_components.items():
            if not item:
                errors.append(f"Warning! You haven't added a {name} to the current build!")

        if self.cpu and not self.cpu.has_integrated_gpu and not self.gpu:
            errors.append(f"No graphics output! Your GPU is missing "
                          f"and the selected CPU does not have integrated graphics. "
                          f"Please add GPU or change your CPU.")

        if errors:
            errors.append("Further compatibility checks are blocked until all components are selected.")
            return errors

        if self.cpu and self.motherboard:
            if self.cpu.socket != self.motherboard.socket:
                errors.append(
                    f"Incompatible sockets! The processor has {self.cpu.socket}, "
                    f"motherboard - {self.motherboard.socket}"
                )
        if self.psu:
            total_consumption = 0
            for comp in [self.cpu, self.ram, self.motherboard, self.gpu]:
                if comp:
                    if comp == self.ram and self.ram_count:
                        total_consumption += comp.power * int(self.ram_count)
                    else:
                        total_consumption += comp.power
            recommended_power = total_consumption * 1.2
            if self.psu.power < recommended_power:
                errors.append(
                    f"Weak power supply unit! Your system consumes approx {total_consumption}W, "
                    f"recommended power is {int(recommended_power)}W, chosen PSU has only {self.psu.power}W."
                )
        if self.ram and self.motherboard:
            if self.ram.ram_type != self.motherboard.ram_type:
                errors.append(f"Memory types for RAM and motherboard do not match. "
                              f"Motherboard has {self.motherboard.ram_type}, "
                              f"RAM has {self.ram.ram_type}")
            if self.ram_count and int(self.ram_count) > self.motherboard.ram_slots:
                errors.append(f"Too many RAM sticks has been added to build! "
                              f"Chosen motherboard can contain only {self.motherboard.ram_slots} sticks of RAM.")

        return errors

    def export_to_txt(self, filename="pc_build.txt"):
        if self.check_compatibility():
            return False
        with open(filename, "w", encoding="utf-8") as file:
            file.write("========================================\n")
            file.write("         YOUR CUSTOM PC RECEIPT         \n")
            file.write("========================================\n")
            file.write(f"• CPU: {self.cpu.name}\n")
            file.write(f"• Motherboard: {self.motherboard.name}\n")
            file.write(f"• RAM: {self.ram.name} x{self.ram_count}\n")
            file.write(f"• GPU: {self.gpu.name if self.gpu else 'Integrated Graphics'}\n")
            file.write(f"• Power Supply: {self.psu.name}\n")
            file.write("----------------------------------------\n")
            file.write(f"TOTAL PRICE: {self.calculate_total_price()}\n")
            file.write("========================================\n")
        return True
