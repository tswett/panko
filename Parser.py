from lark import Lark, Transformer, v_args

from PankoBool import PankoTrue
from PankoFunction import PankoFunction, PushPrimitiveInstruction
from PankoObject import PankoObject

grammar = """
    ?start: "return" atom ";" -> primitive_to_function

    ?atom: "true" -> true

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