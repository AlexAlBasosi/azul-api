from .pattern_line import PatternLine
from ..tile import Tile

class Board:
    """
    The Board class follows the Facade pattern, handling instantiation and methods associated with its sub-components.
    """

    __pattern_lines: PatternLine

    def __init__(self) -> None:
        self.__pattern_lines = PatternLine()

    def place_tile_onto_pattern_line(self, tiles: list[Tile], tile_type: str, line_index: int) -> None:
        """
        Board method that places the tiles onto the pattern line. This is the method that's called from the Game library.

        The actual logic is found within the PatternLine class.
        """
        returned_line: list[Tile] = self.__pattern_lines.place_tile_onto_pattern_line(tiles, tile_type, line_index)
        print(f"{returned_line = }")