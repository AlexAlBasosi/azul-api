"""
Module containing the PatternLine class implementation.
"""

from collections import deque
from collections.abc import Iterator
from ..tile import Tile
from ..rule_error import RuleError


class PatternLine:
    """
    The PatternLine class handles methods associated with adding and removing Tiles from the pattern lines.
    """

    __pattern_lines: list[deque[Tile]]

    def __init__(self) -> None:
        """
        The constructor method generates a list of double-ended queues for each pattern line.
        """
        self.__pattern_lines: list[deque[Tile]] = []

        # A double-ended queue of ascending max-lengths from 1-5 is created, each being appended to the list.
        for line_length in range(1, 6):
            pattern_line: deque[Tile] = deque(maxlen=line_length)
            self.__pattern_lines.append(pattern_line)

    def __iter__(self) -> Iterator[list[Tile]]:
        """
        Dunder method that iterates through the pattern lines and returns each one as a list.
        """
        for pattern_line in self.__pattern_lines:
            yield list(pattern_line)

    def _is_type_in_line(self, tile_type: str, line: deque[Tile]) -> bool:
        """
        Method that checks whether the specified type of tile is in a pattern line.

        If it is, it returns true. Otherwise it returns false.
        """
        for line_tile in line:
            if tile_type != line_tile:
                return False
        return True

    def is_line_full(self, line_index: int) -> bool:
        """
        Method that takes the pattern line index and checks if the corresponding pattern line is full.

        If so, it returns True. Otherwise, it returns False.
        """
        # If the length of the tiles in the pattern lines is not the max length, then the line isn't full, and it returns False.
        if (
            len(self.__pattern_lines[line_index])
            != self.__pattern_lines[line_index].maxlen
        ):
            return False
        # Otherwise, it returns True.
        return True

    def get_tile_type(self, line_index: int) -> str:
        """
        Method that takes the pattern line index and checks the type of the last element within the pattern line.

        It then returns the type.
        """
        # This returns the type of tile of the last element in the selected pattern line.
        return repr(self.__pattern_lines[line_index][-1])

    def place_tile_onto_pattern_line(
        self, tiles: list[Tile], tile_type: str, line_index: int
    ) -> list[Tile]:
        """
        A method that takes a list of tiles to be placed on the pattern line, the type of tiles in that list, and the index of the pattern line
        you want to add the tiles to.

        It then returns the updated pattern line as a list.
        """
        # Validation to ensure there isn't a tile that is a different type in the pattern line selected.
        if not self._is_type_in_line(
            tile_type, self.__pattern_lines[line_index]
        ):
            raise RuleError(
                {
                    "class": "PatternLine",
                    "method": "place_tile_onto_pattern_line",
                    "message": "Pattern Line contains a Tile type of a different colour. You can only place Tiles of the same colour onto the line.",
                }
            )
        max_length: int | None = self.__pattern_lines[line_index].maxlen
        line_length: int | None = len(self.__pattern_lines[line_index])
        tile_length: int | None = len(tiles)

        # This ensures that the lengths aren't None. Mainly to make the type-checker happy :)
        if max_length is not None and line_length is not None:
            space_remaining: int | None = max_length - line_length

        if tile_length is not None and space_remaining is not None:
            # If there isn't enough space for the tiles in the pattern line, it will throw an error.
            if space_remaining == 0:
                raise OverflowError(
                    {
                        "class": "PatternLine",
                        "method": "place_tile_onto_pattern_line",
                        "message": f"Selected Pattern Line only has {space_remaining} space(s) remaining! Please try again but with less Tiles.",
                    }
                )
            # If the space remaining isn't 0, but there are some spaces available, then fill those spaces.
            if tile_length > space_remaining:
                self.__pattern_lines[line_index].extendleft(
                    tiles[:space_remaining]
                )
            # Otherwise, fill the pattern tiles with all the tiles.
            else:
                self.__pattern_lines[line_index].extendleft(tiles)
        # And return the tiles that were added to the pattern line as a list.
        return list(self.__pattern_lines[line_index].copy())

    def clear_pattern_line(self, line_index: int) -> list[Tile]:
        """
        Method that takes the line index, and clears the pattern line.

        It returns a list of tiles to be added to the lid.
        """
        # Validation to ensure that the line is full before being cleared.
        if not self.is_line_full(line_index):
            raise RuleError(
                {
                    "class": "PatternLine",
                    "method": "clear_pattern_line",
                    "message": "Cannot clear pattern line if line is not full.",
                }
            )

        # Removes last element that was added to the wall.
        self.__pattern_lines[line_index].pop()

        returned_tiles: list[Tile] = []
        if len(self.__pattern_lines[line_index]) > 0:
            # Pops remaining elements in pattern line to be returned.
            for _ in range(len(self.__pattern_lines[line_index])):
                returned_tiles.append(self.__pattern_lines[line_index].pop())

        return returned_tiles
