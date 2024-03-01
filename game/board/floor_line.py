"""
Module containing the FloorLine class implementation.
"""

from collections import deque
from collections.abc import Iterator
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

    def __iter__(self) -> Iterator[Tile]:
        """
        Dunder method that iterates through the floor line and returns it.
        """
        for tile in self.__floor_line:
            yield tile

    def place_tiles_onto_floor_line(
        self, *, tiles: list[Tile]
    ) -> list[Tile] | None:
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
            if tile_length <= 0:
                raise IndexError(
                    {
                        "class": "FloorLine",
                        "method": "place_tiles_onto_floor_line",
                        "message": "You must place at least one tile onto the floor line!",
                    }
                )

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

    def calculate_score(self) -> int:
        """
        Method that calculates the negative score incurred by tiles being in the floor line.

        It then returns that score.
        """
        score: int = 0
        # If length of floor line is 0, the score is 0.
        if len(self.__floor_line) == 0:
            return 0
        # Otherwise, 
        else:
            # For each item in the floor line,
            for index in range(len(self.__floor_line)):
                # The associated value of the score attribute, which contains the penalties, is incremented to the score.
                score += self.__scores[index]

        # That score is then returned.
        return score
