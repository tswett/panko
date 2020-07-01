import logging
from typing import Sequence

from PankoObject import PankoObject

class PankoBool(PankoObject):
    def send_message_positional(
        self, msg_name: bytes, arguments: Sequence[PankoObject]) -> PankoObject:

        logging.debug(f'PankoBool received message: {msg_name}')
        logging.debug(f'PankoBool self is: {self}')
        logging.debug(f'PankoBool message arguments: {arguments}')

        if msg_name == b'if_else_v':
            true_value, false_value = arguments
            return self.if_else_v(true_value, false_value)
        else:
            raise ValueError('The given message name was not recognized.')

    def if_else_v(self, true_value: PankoObject, false_value: PankoObject) -> PankoObject:
        raise NotImplementedError

class PankoTrue(PankoBool):
    def __eq__(self, other):
        return isinstance(other, PankoTrue)

    def __repr__(self):
        return "Panko boolean 'true'"

    def if_else_v(self, true_value: PankoObject, false_value: PankoObject) -> PankoObject:
        return true_value

class PankoFalse(PankoBool):
    def __eq__(self, other):
        return isinstance(other, PankoFalse)

    def __repr__(self):
        return "Panko boolean 'false'"

    def if_else_v(self, true_value, false_value):
        return false_value

panko_true = PankoTrue()
panko_false = PankoFalse()