from typing import Any


class Tile:
    """
    Class responsible for the creation of Tiles.
    """

    def __init__(self, colour: str) -> None:
        self.colour = colour

    def getattr(self) -> str:
        return self.colour

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, str):
            return NotImplemented
        return self.colour == other

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, str):
            return NotImplemented
        return self.colour != other
