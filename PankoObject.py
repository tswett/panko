from __future__ import annotations

from typing import Sequence


class PankoObject:
    def send_message_positional(
        self, msg_name: bytes, arguments: Sequence[PankoObject]
    ) -> PankoObject:

        """Send the given named message to this object, passing the given list of arguments as
        named parameters.
        """

        raise NotImplementedError

    def call(self, arguments: Sequence[PankoObject]) -> PankoObject:
        """Call this object, passing the given list of arguments as named parameters."""

        raise NotImplementedError
