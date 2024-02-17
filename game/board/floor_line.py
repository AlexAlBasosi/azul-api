from collections import deque
from ..tile import Tile

class FloorLine:
    """
    The FloorLine class handles methods associated with adding and removing tiles from the floor line.
    """

    __floor_line: deque[Tile]
    __scores: tuple[int, ...]

    def __init__(self) -> None:
        self.__scores = tuple([-1, -1, -2, -2, -2, -3, -3])
        self.__floor_line = deque(maxlen=7)

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
