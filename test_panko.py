import logging
import sys
from typing import Mapping
import unittest

from typeguard.importhook import install_import_hook

install_import_hook("panko")

from panko import parser
from panko.functions import BuiltinFunction, PankoFunction, PushPrimitiveInstruction
from panko.objects import PankoFalse, PankoInteger, PankoObject, PankoTrue


def quick_test(
    test_case: unittest.TestCase,
    function_body: str,
    expected_result: PankoObject,
    globals: Mapping[bytes, PankoObject] = None,
):
    function = parser.parse_function_body(function_body)
    function.globals = globals
    result = function.call(arguments=[])
    test_case.assertEqual(result, expected_result)


class BasicTests(unittest.TestCase):
    def test_constant_function(self):
        instruction_list = [PushPrimitiveInstruction(PankoTrue())]
        function = PankoFunction(instruction_list)
        result = function.call(arguments=[])
        self.assertEqual(result, PankoTrue())

    def test_parse_constant_function(self):
        quick_test(self, "return true;", PankoTrue())

    def test_need_space_after_keyword(self):
        with self.assertRaises(BaseException):
            parser.parse_function_body("returntrue;")

    def test_send_message(self):
        quick_test(self, "return false.if_else_v(false, false);", PankoFalse())
        quick_test(self, "return false.if_else_v(false, true);", PankoTrue())
        quick_test(self, "return false.if_else_v(true, false);", PankoFalse())
        quick_test(self, "return false.if_else_v(true, true);", PankoTrue())
        quick_test(self, "return true.if_else_v(false, false);", PankoFalse())
        quick_test(self, "return true.if_else_v(false, true);", PankoFalse())
        quick_test(self, "return true.if_else_v(true, false);", PankoTrue())
        quick_test(self, "return true.if_else_v(true, true);", PankoTrue())

    def test_parse_integer(self):
        quick_test(self, "return 5;", PankoInteger(5))

    def test_argument_order(self):
        quick_test(
            self, "return true.if_else_v(1, true.if_else_v(2, 3));", PankoInteger(1)
        )
        quick_test(
            self, "return true.if_else_v(1, false.if_else_v(2, 3));", PankoInteger(1)
        )
        quick_test(
            self, "return false.if_else_v(1, true.if_else_v(2, 3));", PankoInteger(2)
        )
        quick_test(
            self, "return false.if_else_v(1, false.if_else_v(2, 3));", PankoInteger(3)
        )
        quick_test(
            self, "return true.if_else_v(true.if_else_v(1, 2), 3);", PankoInteger(1)
        )
        quick_test(
            self, "return true.if_else_v(false.if_else_v(1, 2), 3);", PankoInteger(2)
        )
        quick_test(
            self, "return false.if_else_v(true.if_else_v(1, 2), 3);", PankoInteger(3)
        )
        quick_test(
            self, "return false.if_else_v(false.if_else_v(1, 2), 3);", PankoInteger(3)
        )

    def test_globals(self):
        globals = {b"three": PankoInteger(3)}
        quick_test(self, "return three;", PankoInteger(3), globals=globals)

    def test_builtin_function(self):
        plus_one = BuiltinFunction(lambda x: PankoInteger(x.value + 1))
        globals = {b"plus_one": plus_one}
        quick_test(self, "return plus_one(8);", PankoInteger(9), globals=globals)

    def test_builtin_argument_order(self):
        first = BuiltinFunction(lambda x, y: x)
        second = BuiltinFunction(lambda x, y: y)
        globals = {b"first": first, b"second": second}

        def quicker_test(body, int):
            quick_test(self, body, PankoInteger(int), globals=globals)

        quicker_test("return first(1, first(2, 3));", 1)
        quicker_test("return first(1, second(2, 3));", 1)
        quicker_test("return second(1, first(2, 3));", 2)
        quicker_test("return second(1, second(2, 3));", 3)
        quicker_test("return first(first(1, 2), 3);", 1)
        quicker_test("return first(second(1, 2), 3);", 2)
        quicker_test("return second(first(1, 2), 3);", 3)
        quicker_test("return second(second(1, 2), 3);", 3)


if __name__ == "__main__":
    # logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    unittest.main()
