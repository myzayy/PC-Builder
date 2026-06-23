'''
Compatibility check logic
'''

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
        components = [self.cpu, self.ram, self.motherboard, self.gpu, self.psu]
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
            if self.ram_count > self.motherboard.ram_slots:
                errors.append(f"Too many RAM sticks has been added to build! "
                              f"Chosen motherboard can contain only {self.motherboard.ram_slots} sticks of RAM.")

        return errors
