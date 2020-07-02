from __future__ import annotations

from typing import Callable, List, Mapping, Optional, Sequence

from .objects import PankoObject


class ExecutionContext:
    def __init__(
        self,
        stack: List[PankoObject],
        positionals: Sequence[PankoObject],
        globals: Mapping[bytes, PankoObject] = None,
    ):
        self.stack = stack
        self.positionals = positionals
        self.globals = globals or {}


class PankoInstruction:
    def execute(self, context: ExecutionContext):
        raise NotImplementedError


class PushGlobalInstruction(PankoInstruction):
    def __init__(self, global_name: bytes):
        self.global_name = global_name

    def __repr__(self):
        return f"push_global({self.global_name!s})"

    def execute(self, context: ExecutionContext):
        value = context.globals[self.global_name]
        context.stack.append(value)


class PushPrimitiveInstruction(PankoInstruction):
    def __init__(self, value: PankoObject):
        self.value = value

    def __repr__(self):
        return f"push({self.value})"

    def execute(self, context: ExecutionContext):
        context.stack.append(self.value)


class CallInstruction(PankoInstruction):
    def __init__(self, num_arguments: int):
        self.num_arguments = num_arguments

    def __repr__(self):
        return f"call({self.num_arguments})"

    def execute(self, context: ExecutionContext):
        arguments = context.stack[-self.num_arguments :]
        for _ in range(self.num_arguments):
            context.stack.pop()
        target = context.stack.pop()
        result = target.call(arguments)
        context.stack.append(result)


class SendMessageInstruction(PankoInstruction):
    def __init__(self, message_name: bytes, num_arguments: int):
        self.message_name = message_name
        self.num_arguments = num_arguments

    def __repr__(self):
        return f"send_message({self.message_name}, {self.num_arguments})"

    def execute(self, context: ExecutionContext):
        arguments = context.stack[-self.num_arguments :]
        for _ in range(self.num_arguments):
            context.stack.pop()
        target = context.stack.pop()
        result = target.send_message_positional(self.message_name, arguments)
        context.stack.append(result)


class PankoFunction(PankoObject):
    def __init__(self, instructions: Sequence[PankoInstruction]):
        self.instructions = instructions
        self.globals = None  # type: Optional[Mapping[bytes, PankoObject]]

    def __repr__(self):
        return repr(self.instructions)

    def call(self, arguments: Sequence[PankoObject]) -> PankoObject:
        context = ExecutionContext(
            stack=[], positionals=list(arguments), globals=self.globals
        )

        for instruction in self.instructions:
            instruction.execute(context)

        return context.stack[-1]


class BuiltinFunction(PankoObject):
    def __init__(self, implementation: Callable[..., PankoObject]):
        self.implementation = implementation

    def call(self, arguments: Sequence[PankoObject]):
        return self.implementation(*arguments)
