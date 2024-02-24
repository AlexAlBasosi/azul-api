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

    def _count_adjacent_row_items(
        self, row_index: int, column_index: int
    ) -> int:
        consecutive_count: int = 0

        # Count consecutive items to the left of the selected item, EXCLUDING item
        for index in range(column_index - 1, -1, -1):
            if self.__wall[row_index][index][1] is not None:
                consecutive_count += 1
            else:
                break

        # Count consecutive items to the right of the selected item
        for index in range(column_index + 1, len(self.__wall[row_index])):
            if self.__wall[row_index][index][1] is not None:
                consecutive_count += 1
            else:
                break

        return consecutive_count

    def _count_adjacent_column_items(
        self, row_index: int, column_index: int
    ) -> int:
        consecutive_count: int = 0

        # Count consecutive items above the selected item, EXCLUDING item
        for index in range(row_index - 1, -1, -1):
            if self.__wall[index][column_index][1] is not None:
                consecutive_count += 1
            else:
                break

        # Count consecutive items below the selected item
        for index in range(row_index + 1, len(self.__wall)):
            if self.__wall[index][column_index][1] is not None:
                consecutive_count += 1
            else:
                break

        return consecutive_count

    def place_tile_onto_wall(
        self, row: int, column: int, tile_type: str
    ) -> int:
        """
        Method that takes in the row index and the column index, and places the item onto the wall.

        It then returns the score.
        """
        score: int = 0
        self.__wall[row][column][1] = Tile(tile_type)

        row_score: int = self._count_adjacent_row_items(row, column)
        column_score: int = self._count_adjacent_column_items(row, column)

        # consecutive items in the row (excluding item) + consecutive items in the column (excluding item) + item itself
        score = row_score + column_score + 1

        return score

    def is_row_full(self) -> bool:
        """
        Method that iterates through each of the rows and checks if any of the rows are full.

        If so, it returns True. Otherwise, it returns False.
        """
        for row_index in range(self.__rows):
            count: int = 0
            for column_index in range(self.__columns):
                if self.__wall[row_index][column_index][1] is not None:
                    count += 1
            if count == 5:
                return True
        return False

    def count_full_rows(self) -> int:
        """
        Method that iterates through each of the rows and checks if they're full.

        It returns a count of full rows.
        """
        full_row_count: int = 0

        for row_index in range(self.__rows):
            consecutive_count: int = 0
            for column_index in range(self.__columns):
                if self.__wall[row_index][column_index][1] is not None:
                    consecutive_count += 1
            if consecutive_count == 5:
                full_row_count += 1
        return full_row_count

    def count_full_columns(self) -> int:
        """
        Method that iterates through each of the columns and checks if they're full.

        It returns a count of full columns.
        """
        full_column_count: int = 0

        for row_index in range(self.__rows):
            consecutive_count: int = 0
            for column_index in range(self.__columns):
                if self.__wall[column_index][row_index][1] is not None:
                    consecutive_count += 1
            if consecutive_count == 5:
                full_column_count += 1
        return full_column_count

    def count_full_tiles(self) -> int:
        """
        Method that iterates through each of the rows and columns diagonally and checks if it has a full row of tiles.

        It returns a count of diagonal tiles.
        """
        full_tile_count: int = 0

        for row_index in range(self.__rows):
            consecutive_count: int = 0
            for column_index in range(self.__columns):
                if (
                    self.__wall[column_index][
                        (row_index + column_index) % self.__rows
                    ][1]
                    is not None
                ):
                    consecutive_count += 1
            if consecutive_count == 5:
                full_tile_count += 1
        return full_tile_count
