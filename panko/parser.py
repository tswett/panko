import logging
from typing import cast, Sequence

from lark import Lark, Transformer, v_args
from lark.lexer import Token

from .functions import (
    CallInstruction,
    PankoFunction,
    PankoInstruction,
    PushGlobalInstruction,
    PushPrimitiveInstruction,
    SendMessageInstruction,
)
from .objects import PankoFalse, PankoInteger, PankoObject, PankoTrue

grammar = r"""
    start: _RETURN expression _SEMICOLON -> instructions_to_function

    ?expression: primitive_atom -> push_primitive
               | IDENTIFIER -> push_global
               | expression _DOT IDENTIFIER _LEFTPAREN argument_list _RIGHTPAREN -> send_message
               | expression _LEFTPAREN argument_list _RIGHTPAREN -> call

    argument_list: (expression (_COMMA expression)*)? -> get_argument_list

    primitive_atom: _FALSE -> false
        | _TRUE -> true
        | INTEGER -> integer

    _COMMA.5: ","
    _DOT.5: "."
    _LEFTPAREN.5: "("
    _RIGHTPAREN.5: ")"
    _SEMICOLON.5: ";"

    _FALSE.7: /false(?!\w)/
    _RETURN.7: /return(?!\w)/
    _TRUE.7: /true(?!\w)/

    IDENTIFIER.5: /[A-Za-z_][A-Za-z0-9_]*(?!\w)/
    INTEGER.5: /[0-9]+(?!\w)/

    %import common.WS_INLINE
    %ignore WS_INLINE
"""


@v_args(inline=True)
class PankoTransformer(Transformer):
    def get_argument_list(self, *arguments):
        logging.debug(f"flatten_argument_list: received {arguments}")
        return arguments

    def false(self):
        return PankoFalse()

    def true(self):
        return PankoTrue()

    def integer(self, value_token: Token):
        return PankoInteger(int(value_token))

    def instructions_to_function(self, instruction_list: Sequence[PankoInstruction]):
        return PankoFunction(instruction_list)

    def push_global(self, global_name: Token):
        global_name_bytes = bytes(str(global_name), "utf8")
        return [PushGlobalInstruction(global_name_bytes)]

    def push_primitive(self, primitive: PankoObject):
        return [PushPrimitiveInstruction(primitive)]

    def send_message(
        self,
        target: Sequence[PankoInstruction],
        message_name: str,
        argument_list: Sequence[Sequence[PankoInstruction]],
    ):
        logging.debug(f"send_message: argument_list is: {argument_list}")
        setup_instructions = list(target) + [
            instruction for argument in argument_list for instruction in argument
        ]
        message_name_bytes = bytes(message_name, "ascii")
        send_message_instruction = SendMessageInstruction(
            message_name_bytes, len(argument_list)
        )
        return setup_instructions + [send_message_instruction]

    def call(
        self,
        target: Sequence[PankoInstruction],
        argument_list: Sequence[Sequence[PankoInstruction]],
    ):
        setup_instructions = list(target) + [
            instruction for argument in argument_list for instruction in argument
        ]
        call_instruction = CallInstruction(len(argument_list))
        return setup_instructions + [call_instruction]


panko_parser = Lark(grammar, parser="lalr", transformer=PankoTransformer())


def parse_function_body(body: str) -> PankoFunction:
    return cast(PankoFunction, panko_parser.parse(body))
