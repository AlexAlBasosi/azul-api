import numpy as np
from ..tile import Tile


class Wall:
    """
    The Wall class handles methods associated with adding and removing tiles from the floor line.
    """

    __rows: int = 5
    __columns: int = 5
    __depth: int = 2
    __wall = np.empty((__rows, __columns, __depth), dtype=object)

    def _shift_right(self, tiles_list: list[str | None]) -> list[str | None]:
        """
        Method that takes in a list of tile types, and shifts them one to the right.

        It then returns the shifted list.
        """
        shifted_list: list[str | None] = [None] * len(tiles_list)
        for index, _ in enumerate(tiles_list):
            shifted_list[(index + 1) % len(tiles_list)] = tiles_list[index]
        return shifted_list

    def __init__(self) -> None:
        """
        Constructor method that initalises the items on the wall.
        """
        self.__wall = np.empty(
            (self.__rows, self.__columns, self.__depth), dtype=object
        )

        tiles_list: list[str | None] = ["blue", "yellow", "red", "black", "ice"]
        for i in range(self.__rows):
            for j in range(self.__columns):
                wall_item: list[str | Tile | None] = [tiles_list[j], None]
                self.__wall[i][j] = wall_item
            tiles_list = self._shift_right(tiles_list)

    def return_wall(self) -> list[list[list[str | Tile | None]]]:
        """
        Method that iterates through the array and appends each row to a list.

        The list is then returned.
        """
        wall: list[list[list[str | Tile | None]]] = []
        for i in range(self.__rows):
            wall_row: list[list[str | Tile | None]] = []
            for j in range(self.__columns):
                wall_item: list[str | Tile | None] = list(self.__wall[i][j])
                wall_row.append(wall_item)
            wall.append(wall_row)
        return wall

    # TODO: refactor this method to call get_column_index
    def is_tile_on_wall(self, line_index: int, tile_type: str) -> bool:
        """
        Method that takes in the pattern line index and the type of tile, and checks if a corresponding tile exists on the wall.

        If it does, it returns True. Otherwise, it returns False.
        """
        for wall_row in self.__wall[line_index]:
            if wall_row[0] == tile_type:
                if wall_row[1] is not None:
                    return True
        return False

    def get_column_index(self, line_index: int, tile_type: str) -> int:
        """
        Method that takes the pattern line index and the type of tile, and retrieves the index of the column.

        It then returns that column index.
        """
        index: int = 0
        for i, wall_row in enumerate(self.__wall[line_index]):
            if repr(wall_row[0]) == tile_type:
                index = i

        return index

    def place_tile_onto_wall(
        self, row: int, column: int, tile_type: str
    ) -> None:
        self.__wall[row][column][1] = Tile(tile_type)

        # TODO: add logic to calculate the score and return to board
