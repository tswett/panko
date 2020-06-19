from __future__ import annotations

from PankoObject import PankoObject

class PankoTable(PankoObject):
    @staticmethod
    def from_sequence(sequence: Sequence[PankoObject]) -> PankoTable:
        # To do: make this actually work.
        return PankoTable()