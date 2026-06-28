"""
All component classes
"""

class Component:
    def __init__(self, name: str, price: float, power: int):
        self.name = name
        self.price = price
        self.power = power # consumption for parts, or power for the power supply

class CPU(Component):
    def __init__(self, name, price, power, socket: str, has_integrated_gpu: bool):
        super().__init__(name, price, power)
        self.socket = socket
        self.has_integrated_gpu = has_integrated_gpu

class Motherboard(Component):
    def __init__(self, name, price, power, socket: str, ram_type: str, ram_slots: int):
        super().__init__(name, price, power)
        self.socket = socket
        self.ram_type = ram_type
        self.ram_slots = ram_slots

class GPU(Component):
    def __init__(self, name, price, power):
        super().__init__(name, price, power)

class PSU(Component):
    def __init__(self, name, price, power):
        super().__init__(name, price, power) # ex. power = 750W

class RAM(Component):
    def __init__(self, name, price, power, ram_type: str):
        super().__init__(name, price, power)
        self.ram_type = ram_type
