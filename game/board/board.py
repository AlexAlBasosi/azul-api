from .pattern_line import PatternLine
from ..tile import Tile
from collections import deque

class Board:
    """
    The Board class follows the Facade pattern, handling instantiation and methods associated with its sub-components.
    """

    __pattern_lines: PatternLine
    __floor_line: deque[Tile]
    __scores: tuple[int, ...]

    def __init__(self) -> None:
        self.__pattern_lines = PatternLine()
        self.__scores = tuple([-1, -1, -2, -2, -2, -3, -3])
        self.__floor_line = deque(maxlen=7)
        
    def place_tile_onto_pattern_line(self, tiles: list[Tile], tile_type: str, line_index: int) -> None:
        """
        Board method that places the tiles onto the pattern line. This is the method that's called from the Game library.

        The actual logic is found within the PatternLine class.
        """
        returned_line: list[Tile] = self.__pattern_lines.place_tile_onto_pattern_line(tiles, tile_type, line_index)
        print(f"{returned_line = }")

    #TODO: Refactor the below into a separate class.
    def place_tiles_onto_floor_line(self, *, tiles: list[Tile]) -> list[Tile] | None:
        """
        Board method that takes the tiles to be added to the floor line. If there's space remaining in the floor line, it will be added, and None
        will be returned.

        Otherwise, it will add the tiles up to the limit and return the rest.
        """
        max_length: int | None = self.__floor_line.maxlen
        line_length: int | None = len(self.__floor_line)
        tile_length: int | None = len(tiles)

        # This ensures that the lengths aren't None. Mainly to make the type-checker happy :)
        if max_length is not None and line_length is not None:
            space_remaining: int | None = max_length - line_length

        if tile_length is not None and space_remaining is not None:
            # If the space remaining is 0, it will return all the tiles to be added to the lid.
            if space_remaining == 0:
                return tiles
            # If the tile length is less than the space remaining, all the tiles will be added to the floor line.
            if tile_length < space_remaining:
                self.__floor_line.extend(tiles)
            # If the tile length is greater than or equal to the space remaining, it will add that many tiles to the floor line and return the
            # rest.
            elif tile_length >= space_remaining:
                self.__floor_line.extend(tiles[:space_remaining])
                return tiles[space_remaining:]
        return None

    #TODO look into why black isn't formatting this file