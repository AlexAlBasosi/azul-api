from .pattern_line import PatternLine
from .floor_line import FloorLine
from ..tile import Tile

class Board:
    """
    The Board class follows the Facade pattern, handling instantiation and methods associated with its sub-components.
    """

    __pattern_lines: PatternLine
    __floor_line: FloorLine

    def __init__(self) -> None:
        self.__pattern_lines = PatternLine()
        self.__floor_line = FloorLine()

    def return_pattern_lines(self) -> list[list[Tile]]:
        """
        Method that returns a list of the pattern lines and the tiles within them. 
        """
        pattern_lines: list[list[Tile]] = [line_tiles for line_tiles in iter(self.__pattern_lines)]

        return pattern_lines
    
    def return_floor_line(self) -> list[str]:
        """
        Method that returns a list of the floor line tiles.
        """
        floor_line: list[str] = [tile.getattr() for tile in iter(self.__floor_line)]

        return floor_line
        
    def place_tile_onto_pattern_line(self, tiles: list[Tile], tile_type: str, line_index: int) -> None:
        """
        Board method that places the tiles onto the pattern line. This is the method that's called from the Game library.

        The actual logic is found within the PatternLine class.
        """
        self.__pattern_lines.place_tile_onto_pattern_line(tiles, tile_type, line_index)

    def place_tiles_onto_floor_line(self, *, tiles: list[Tile]) -> list[Tile] | None:
        """
        Board method that takes the tiles to be added to the floor line. If there's space remaining in the floor line, it will be added, and None
        will be returned.

        Otherwise, it will add the tiles up to the limit and return the rest.
        """
        
        return self.__floor_line.place_tiles_onto_floor_line(tiles=tiles)

    #TODO look into why black isn't formatting this file