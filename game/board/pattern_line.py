from collections import deque
from collections.abc import Iterator
from ..tile import Tile


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
        # TODO: figure out why != on tiles isn't working
        for line_tile in line:
            if tile_type != line_tile:
                return False
        return True

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
            raise TypeError(
                "Pattern Line contains a Tile type of a different colour. You can only place Tiles of the same colour onto the line."
            )
        max_length: int | None = self.__pattern_lines[line_index].maxlen
        line_length: int | None = len(self.__pattern_lines[line_index])
        tile_length: int | None = len(tiles)

        # This ensures that the lengths aren't None. Mainly to make the type-checker happy :)
        if max_length is not None and line_length is not None:
            space_remaining: int | None = max_length - line_length

        if tile_length is not None and space_remaining is not None:
            # If there isn't enough space for the tiles in the pattern line, it will throw an error.
            if tile_length > space_remaining:
                raise OverflowError(
                    f"Selected Pattern Line only has {space_remaining} space(s) remaining! Please try again but with less Tiles."
                )

            self.__pattern_lines[line_index].extendleft(tiles)

        return list(self.__pattern_lines[line_index].copy())
