from PankoObject import PankoObject

class PankoInteger(PankoObject):
    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, PankoInteger) and (self.value == other.value)

    def __repr__(self):
        return f"Panko integer {self.value}"