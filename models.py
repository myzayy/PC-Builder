"""
All component classes
"""

class Component:
    def __init__(self, name: str, price: float, power: int):
        self.name = name
        self.price = price
        self.power = power  # consumption for parts, or power for the power supply


class CPU(Component):
    def __init__(self, name, price, power, socket: str, integrated_gpu: bool, included_cooler: bool):
        super().__init__(name, price, power)
        self.socket = socket
        self.integrated_gpu = integrated_gpu
        self.included_cooler = included_cooler


class Motherboard(Component):
    def __init__(self, name, price, power, socket: str, ram_type: str, ram_slots: int, form_factor: str):
        super().__init__(name, price, power)
        self.socket = socket
        self.ram_type = ram_type
        self.ram_slots = ram_slots
        self.form_factor = form_factor


class GPU(Component):
    def __init__(self, name, price, power, length: int):
        super().__init__(name, price, power)
        self.length = length  # length of graphic card in mm


class PSU(Component):
    def __init__(self, name, price, power):
        super().__init__(name, price, power)  # power = wattage (ex. 750)


class RAM(Component):
    def __init__(self, name, price, power, ram_type: str):
        super().__init__(name, price, power)
        self.ram_type = ram_type


class CPUCooler(Component):
    def __init__(self, name, price, power, height: int, sockets: list):
        super().__init__(name, price, power)
        self.height = height  # cooler height in mm
        self.sockets = sockets  # list of supported sockets (ex. ["AM5", "LGA1700"])


class Case:
    def __init__(self, name: str, price: float, max_gpu_length: int, max_cpu_cooler_height: int, supported_form_factors: list):
        self.name = name
        self.price = price
        self.max_gpu_length = max_gpu_length  # in mm
        self.max_cpu_cooler_height = max_cpu_cooler_height  # in mm
        self.supported_form_factors = supported_form_factors  # ex. ["ATX", "Mini-ITX"]


class Storage(Component):
    def __init__(self, name, price, power):
        super().__init__(name, price, power)
