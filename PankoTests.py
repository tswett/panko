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
        function = Parser.parse_function_body('return true;')
        result = function.call(arguments=[])
        self.assertEqual(result, PankoTrue())
    
    def test_need_space_after_keyword(self):
        with self.assertRaises(BaseException):
            Parser.parse_function_body('returntrue;')

if __name__ == '__main__':
    unittest.main()
