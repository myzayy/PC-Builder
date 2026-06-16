'''
Compatibility check logic
'''

class PCBuild():
    def __init__(self):
        self.cpu = None
        self.motherboard = None
        self.gpu = None
        self.psu = None

    def calculate_total_price(self) -> float:
        components = [self.cpu, self.motherboard, self.gpu, self.psu]
        return sum(item.price for item in components if item is not None)

    def check_compatibility(self) -> list:
        errors = []

        if self.cpu and self.motherboard:
            if self.cpu.socket != self.motherboard.socket:
                errors.append(
                    f"Incompatible sockets! The processor has {self.cpu.socket}, "
                    f"motherboard - {self.motherboard.socket}"
                )
        if self.psu:
            total_consumption = 0
            for comp in [self.cpu, self.motherboard, self.gpu]:
                if comp:
                    total_consumption += comp.power
            recommended_power = total_consumption * 1.2
            if self.psu.power < recommended_power:
                errors.append(
                    f"Weak power supply unit! Your system consumes approx {total_consumption}, "
                    f"recommended power is {int(recommended_power)}W, chosen PSU has only {self.psu.power}W."
                )

        return errors
