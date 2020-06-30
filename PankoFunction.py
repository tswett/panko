from __future__ import annotations

from typing import List, Sequence

from PankoObject import PankoObject

class PankoInstruction:
    def execute(self, stack: List[PankoObject], positionals: Sequence[PankoInstruction]):
        raise NotImplementedError

class PushPrimitiveInstruction(PankoInstruction):
    def __init__(self, value: PankoObject):
        self.value = value

    def __repr__(self):
        return f'push({self.value})'

    def execute(self, stack: List[PankoObject], positionals: Sequence[PankoInstruction]):
        stack.append(self.value)

class PankoFunction(PankoObject):
    def __init__(self, instructions: Sequence[PankoInstruction]):
        self.instructions = instructions
    
    def __repr__(self):
        return repr(self.instructions)
    
    def call(self, arguments: Sequence[PankoObject]) -> PankoObject:
        stack = []
        positionals = list(arguments)

        for instruction in self.instructions:
            instruction.execute(stack, positionals)

        return stack[-1]