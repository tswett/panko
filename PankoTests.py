import logging
import sys
import unittest

from PankoBool import PankoFalse, PankoTrue
from PankoFunction import PankoFunction, PushPrimitiveInstruction
from PankoObject import PankoObject
import Parser

def quick_test(test_case: unittest.TestCase, function_body: str, expected_result: PankoObject):
    function = Parser.parse_function_body(function_body)
    result = function.call(arguments=[])
    test_case.assertEqual(result, expected_result)

class BasicTests(unittest.TestCase):
    def test_constant_function(self):
        instruction_list = [PushPrimitiveInstruction(PankoTrue())]
        function = PankoFunction(instruction_list)
        result = function.call(arguments=[])
        self.assertEqual(result, PankoTrue())
    
    def test_parse_constant_function(self):
        quick_test(self, 'return true;', PankoTrue())
    
    def test_need_space_after_keyword(self):
        with self.assertRaises(BaseException):
            Parser.parse_function_body('returntrue;')
    
    def test_send_message(self):
        quick_test(self, 'return false.if_else_v(false, false);', PankoFalse())
        quick_test(self, 'return false.if_else_v(false, true);', PankoTrue())
        quick_test(self, 'return false.if_else_v(true, false);', PankoFalse())
        quick_test(self, 'return false.if_else_v(true, true);', PankoTrue())
        quick_test(self, 'return true.if_else_v(false, false);', PankoFalse())
        quick_test(self, 'return true.if_else_v(false, true);', PankoFalse())
        quick_test(self, 'return true.if_else_v(true, false);', PankoTrue())
        quick_test(self, 'return true.if_else_v(true, true);', PankoTrue())

if __name__ == '__main__':
    # logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    unittest.main()
