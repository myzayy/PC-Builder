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
        self.storage = None
        self.cpu_cooler = None
        self.case = None

    def calculate_total_price(self) -> float:
        total_price = 0
        components = [self.cpu, self.motherboard, self.gpu, self.psu, self.storage, self.cpu_cooler, self.case]
        for item in components:
            if item:
                total_price += float(item.price)

        if self.ram and self.ram_count:
            total_price += float(self.ram.price) * int(self.ram_count)

        return total_price

    def check_compatibility(self) -> list:
        errors = []

        self._validate_presence(errors)

        if errors:
            errors.append("Further compatibility checks are blocked until all components are selected.")
            return errors

        self._validate_gpu_and_cooling_necessity(errors)
        self._validate_sockets_and_slots(errors)
        self._validate_case_dimensions(errors)
        self._validate_power_supply(errors)
        self._validate_ram_compatibility(errors)


        return errors

    def _validate_presence(self, errors: list):
        required_components = {
            "Processor (CPU)": self.cpu,
            "Motherboard": self.motherboard,
            "RAM": self.ram,
            "Power Supply (PSU)": self.psu,
            "Storage": self.storage,
            "Case": self.case
        }

        for name, item in required_components.items():
            if not item:
                errors.append(f"Warning! You haven't added a {name} to the current build!")

    def _validate_gpu_and_cooling_necessity(self, errors: list):
        if self.cpu and not self.cpu.integrated_gpu and not self.gpu:
            errors.append(f"No graphics output! Your GPU is missing "
                          f"and the selected CPU does not have integrated graphics. "
                          f"Please add GPU or change your CPU.")
        if self.cpu and not self.cpu.included_cooler and not self.cpu_cooler:
            errors.append(f"No CPU cooler in current build! "
                          f"and the selected CPU does not have included cooler. "
                          f"Please add CPU cooler or change your CPU. ")

    def _validate_sockets_and_slots(self, errors: list):
        if self.cpu and self.motherboard:
            if self.cpu.socket != self.motherboard.socket:
                errors.append(
                    f"Incompatible sockets! The processor has {self.cpu.socket}, "
                    f"motherboard - {self.motherboard.socket}"
                )
        if self.cpu_cooler and self.motherboard:
            if self.motherboard.socket not in self.cpu_cooler.sockets:
                sockets_text = ", ".join(self.cpu_cooler.sockets)
                errors.append(
                    f"Cooler doesn't fit! The Motherboard has {self.motherboard.socket}, "
                    f"cooler only works at - {sockets_text} sockets. "
                )

    def _validate_case_dimensions(self, errors: list):
        # Compatibility to fit components in case
        if not self.case:
            return

        if self.motherboard:
            if self.motherboard.form_factor not in self.case.supported_form_factors:
                errors.append("Motherboard form factor doesn't fit in chosen case! ")
        if self.gpu:
            if self.gpu.length > self.case.max_gpu_length:
                errors.append("Your GPU is too long to fit in chosen case! ")
        if self.cpu_cooler:
            if self.cpu_cooler.height > self.case.max_cpu_cooler_height:
                errors.append("Your CPU Cooler is too high to fit in chosen case! ")

    def _validate_power_supply(self, errors: list):

        if not self.psu:
            return

        total_consumption = 0
        for comp in [self.cpu, self.motherboard, self.gpu, self.storage, self.cpu_cooler]:
            if comp:
                total_consumption += comp.power
        if self.ram and self.ram_count:
            total_consumption += self.ram.power * int(self.ram_count)

        recommended_power = total_consumption * 1.2

        if self.psu.power < recommended_power:
            errors.append(
                f"Weak power supply unit! Your system consumes approx {total_consumption}W, "
                f"recommended power is {int(recommended_power)}W, chosen PSU has only {self.psu.power}W."
            )

    def _validate_ram_compatibility(self, errors:list):
        if not (self.ram and self.motherboard):
            return
        if self.ram.ram_type != self.motherboard.ram_type:
            errors.append(f"Memory types for RAM and motherboard do not match. "
                          f"Motherboard has {self.motherboard.ram_type}, "
                          f"RAM has {self.ram.ram_type}")
        if self.ram_count and int(self.ram_count) > self.motherboard.ram_slots:
            errors.append(f"Too many RAM sticks has been added to build! "
                          f"Chosen motherboard can contain only {self.motherboard.ram_slots} sticks of RAM.")

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
            file.write(f"• Storage: {self.storage.name}\n")
            file.write(f"• CPU Cooler: {self.cpu_cooler.name}\n")
            file.write(f"• Case: {self.case.name}\n")
            file.write("----------------------------------------\n")
            file.write(f"TOTAL PRICE: {self.calculate_total_price()}$\n")
            file.write("========================================\n")
        return True
