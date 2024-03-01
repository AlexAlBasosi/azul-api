"""
Module containing the Tile class implementation.
"""

from typing import Any


class Tile:
    """
    Class responsible for the creation of Tiles.
    """

    def __init__(self, colour: str) -> None:
        self.colour = colour

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, str):
            return NotImplemented
        return self.colour == other

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, str):
            return NotImplemented
        return self.colour != other

    def __repr__(self) -> str:
        return self.colour
