import unittest

from PankoBool import PankoTrue
from PankoFunction import PankoFunction, PushPrimitiveInstruction
import Parser

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
