import unittest

from PankoBool import PankoTrue
from PankoFunction import PankoFunction, PushPrimitiveInstruction

class BasicTests(unittest.TestCase):
    def test_constant_function(self):
        panko_true = PankoTrue()
        instruction_list = [PushPrimitiveInstruction(panko_true)]
        function = PankoFunction(instruction_list)
        result = function.call(arguments=[])
        self.assertEqual(result, panko_true)

if __name__ == '__main__':
    unittest.main()
