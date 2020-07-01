from lark import Lark, Transformer, v_args

from PankoBool import PankoTrue
from PankoFunction import PankoFunction, PushPrimitiveInstruction
from PankoObject import PankoObject

grammar = r"""
    start: _RETURN atom _SEMICOLON -> primitive_to_function

    atom: _TRUE -> true

    _SEMICOLON.5: ";"
    _RETURN.7: /return(?!\w)/
    _TRUE.7: /true(?!\w)/

    %import common.WS_INLINE
    %ignore WS_INLINE
"""

@v_args(inline=True)
class PankoTransformer(Transformer):
    def true(self):
        return PankoTrue()

    def primitive_to_function(self, primitive: PankoObject):
        instruction_list = [PushPrimitiveInstruction(primitive)]
        function = PankoFunction(instruction_list)
        return function

panko_parser = Lark(grammar, parser='lalr', transformer=PankoTransformer())
parse_function_body = panko_parser.parse