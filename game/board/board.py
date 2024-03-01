"""
Module containing the Board class implementation.
"""

from .pattern_line import PatternLine
from .floor_line import FloorLine
from .wall import Wall
from ..tile import Tile
from ..rule_error import RuleError


class Board:
    """
    The Board class follows the Facade pattern, handling instantiation and methods associated with pattern lines, the floor line, the wall, and the score.
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

    def _place_tile_onto_wall(self, line_index: int) -> list[Tile]:
        """
        Method that takes the line index of the item to be placed on the wall.

        It then stores the score, clears the pattern line, and returns a list of tiles to be added to the lid.
        """
        # Validation to ensure that the line is full before placing tile onto the wall. If it isn't, it raises a Rule Error.
        if not self.__pattern_lines.is_line_full(line_index):
            raise RuleError(
                {
                    "class": "Board",
                    "method": "place_tile_onto_wall",
                    "message": "Cannot place tile onto wall if pattern line is not empty!",
                }
            )

        # For the specified pattern line, it first gets the tile type in the pattern line.
        tile_type: str = self.__pattern_lines.get_tile_type(line_index)
        # As well as the index of the column of the associated tile type on the wall.
        column_index: int = self.__wall.get_column_index(line_index, tile_type)
        # It then places the tile onto the wall, which returns the score calculated when tile is added to the wall. This is stored as an attribute.
        self.__score += self.__wall.place_tile_onto_wall(
            line_index, column_index, tile_type
        )

        # The pattern line is cleared and the returned items are returned.
        return self.__pattern_lines.clear_pattern_line(line_index)

    def return_pattern_lines(self) -> list[list[Tile]]:
        """
        Method that returns a list of the pattern lines and the tiles within them.
        """
        # This iterates through the pattern lines and returns them as a list of lists.
        pattern_lines: list[list[Tile]] = [
            line_tiles for line_tiles in iter(self.__pattern_lines)
        ]

        return pattern_lines
    
    def return_floor_line(self) -> list[str | Tile]:
        """
        Method that returns a list of the floor line tiles.
        """
        floor_line: list[str | Tile] = []
        # For each item in the floor line,
        for tile in iter(self.__floor_line):
            # The tile type is formatted,
            tile_string: str = repr(tile).replace("'", "")
            # Then added to the list.
            floor_line.append(tile_string)
        # Which is returned as a list.
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
    
    def is_pattern_line_full(self, line_index: int) -> bool:
        """
        Method that takes line index.

        It returns True if pattern line is full. Otherwise, it returns False.
        """
        return self.__pattern_lines.is_line_full(line_index)

    def is_tile_on_wall(self, line_index: int, tile_type: str) -> bool:
        """
        Method that takes in the pattern line index and the type of tile, and checks if a corresponding tile exists on the wall.

        If it does, it returns True. Otherwise, it returns False.
        """
        return self.__wall.is_tile_on_wall(line_index, tile_type)
    
    def is_wall_row_full(self) -> bool:
        """
        Method that iterates through each of the rows and check if any of the rows are full.

        If so, it returns True. Otherwise, it returns False.
        """
        return self.__wall.is_row_full()

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

    def place_tiles_onto_wall(self) -> list[list[Tile]]:
        """
        Method that, for each full pattern line, places the tile onto the wall, stores the score, and then adds the negative score from the floor line.

        It then returns the tiles to be added to the lid.
        """
        cleared_pattern_lines: list[list[Tile]] = []
        # For each pattern line,
        for line_index in range(5):
            # As long as the line is full,
            if self.__pattern_lines.is_line_full(line_index):
                # The rightmost tile is added onto the wall, and the rest of the line is appended to cleared pattern lines.
                cleared_pattern_lines.append(
                    self._place_tile_onto_wall(line_index)
                )

        # The score of the items in the floor line is calculated.
        floor_score: int = self.__floor_line.calculate_score()
        # Which is added to the final score. (Usually a negative number, so it's subtracted).
        total_score: int = self.__score + floor_score

        # If the total score is >= 0, the score is incremented by the floor score.
        if total_score >= 0:
            self.__score += floor_score
        # Otherwise, it remains 0.
        else:
            self.__score = 0

        # The cleared pattern lines is returned.
        return cleared_pattern_lines

    def add_final_scores(self) -> None:
        """
        Method that checks if there are any full rows, columns, or diagonal rows of tiles, multiplies those counts by their respective score weight, adds them up, then adds it to the player's final score.
        """
        # Each full row is counted, and for each full row it's multiplied by 2.
        full_row_count: int = self.__wall.count_full_rows() * 2
        # Each full column is counted, and for each full column it's multiplied by 7.
        full_column_count: int = self.__wall.count_full_columns() * 7
        # Each full diagonal row is counted (for instance, each instance where all tiles of the same colour is on the wall), and then multiplied by 10.
        full_tile_count: int = self.__wall.count_full_tiles() * 10

        # These scores are added,
        final_scores: int = full_row_count + full_column_count + full_tile_count

        # and then stored in the score attribute.
        self.__score += final_scores
