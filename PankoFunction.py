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

    def execute(self, stack: List[PankoObject], positionals: Sequence[PankoObject]):
        stack.append(self.value)

class SendMessageInstruction(PankoInstruction):
    def __init__(self, message_name: bytes, num_arguments: int):
        self.message_name = message_name
        self.num_arguments = num_arguments
    
    def __repr__(self):
        return f'send_message({self.message_name}, {self.num_arguments})'

    def execute(self, stack: List[PankoObject], positionals: Sequence[PankoObject]):
        arguments = stack[-self.num_arguments:]
        for _ in range(self.num_arguments):
            stack.pop()
        target = stack.pop()
        result = target.send_message_positional(self.message_name, arguments)
        stack.append(result)

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