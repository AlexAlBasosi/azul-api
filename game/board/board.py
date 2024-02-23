from .pattern_line import PatternLine
from .floor_line import FloorLine
from .wall import Wall
from ..tile import Tile


class Board:
    """
    The Board class follows the Facade pattern, handling instantiation and methods associated with its sub-components.
    """

    __pattern_lines: PatternLine
    __floor_line: FloorLine
    __wall: Wall
    __score: int

    def __init__(self) -> None:
        self.__pattern_lines = PatternLine()
        self.__floor_line = FloorLine()
        self.__wall = Wall()
        self.__score = 0

    def return_pattern_lines(self) -> list[list[Tile]]:
        """
        Method that returns a list of the pattern lines and the tiles within them.
        """
        pattern_lines: list[list[Tile]] = [
            line_tiles for line_tiles in iter(self.__pattern_lines)
        ]

        return pattern_lines

    def is_pattern_line_full(self, line_index: int) -> bool:
        """
        Method that takes line index.

        It returns True if pattern line is full. Otherwise, it returns False.
        """
        return self.__pattern_lines.is_line_full(line_index)

    def return_floor_line(self) -> list[str | Tile]:
        """
        Method that returns a list of the floor line tiles.
        """
        floor_line: list[str | Tile] = []
        for tile in iter(self.__floor_line):
            tile_string: str = repr(tile).replace("'", "")
            floor_line.append(tile_string)

        return floor_line

    def return_wall(self) -> list[list[list[str | Tile | None]]]:
        """
        Method that iterates through the array and appends each row to a list.

        The list is then returned.
        """
        return self.__wall.return_wall()

    def return_score(self) -> int:
        """
        Method that returns the score.
        """
        return self.__score

    def is_tile_on_wall(self, line_index: int, tile_type: str) -> bool:
        """
        Method that takes in the pattern line index and the type of tile, and checks if a corresponding tile exists on the wall.

        If it does, it returns True. Otherwise, it returns False.
        """
        return self.__wall.is_tile_on_wall(line_index, tile_type)

    def place_tile_onto_pattern_line(
        self, tiles: list[Tile], tile_type: str, line_index: int
    ) -> None:
        """
        Board method that places the tiles onto the pattern line. This is the method that's called from the Game library.

        The actual logic is found within the PatternLine class.
        """
        self.__pattern_lines.place_tile_onto_pattern_line(
            tiles, tile_type, line_index
        )

    def place_tiles_onto_floor_line(
        self, *, tiles: list[Tile]
    ) -> list[Tile] | None:
        """
        Board method that takes the tiles to be added to the floor line. If there's space remaining in the floor line, it will be added, and None
        will be returned.

        Otherwise, it will add the tiles up to the limit and return the rest.
        """

        return self.__floor_line.place_tiles_onto_floor_line(tiles=tiles)

    def _place_tile_onto_wall(self, line_index: int) -> list[Tile]:
        """
        Method that takes the line index of the item to be placed on the wall.

        It then stores the score, clears the pattern line, and returns a list of tiles to be added to the lid.
        """
        if not self.__pattern_lines.is_line_full(line_index):
            raise ValueError(
                "Cannot place tile onto wall if pattern line is not empty!"
            )

        tile_type: str = self.__pattern_lines.get_tile_type(line_index)
        column_index: int = self.__wall.get_column_index(line_index, tile_type)
        self.__score += self.__wall.place_tile_onto_wall(
            line_index, column_index, tile_type
        )

        return self.__pattern_lines.clear_pattern_line(line_index)
    
    def place_tiles_onto_wall(self) -> list[list[Tile]]:
        """
        Method that, for each full pattern line, places the tile onto the wall, stores the score, and then adds the negative score from the floor line.

        It then returns the tiles to be added to the lid.
        """
        cleared_pattern_lines: list[list[Tile]] = []
        for line_index in range(5):
            if self.__pattern_lines.is_line_full(line_index):
                cleared_pattern_lines.append(self._place_tile_onto_wall(line_index))
        
        floor_score: int = self.__floor_line.calculate_score()
        total_score: int = self.__score + floor_score

        if total_score >= 0:
            self.__score += floor_score
        else:
            self.__score = 0

        return cleared_pattern_lines