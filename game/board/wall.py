"""
Module containing the Wall class implementation.
"""

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
        # For each index in the tiles list,
        for index, _ in enumerate(tiles_list):
            # We shift it one to the right, and mod it by the length of tiles list so it wraps around to the beginning.
            shifted_list[(index + 1) % len(tiles_list)] = tiles_list[index]

        # The shifted list is returned.
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
                # For each row, and column in range 5, we initialise a list with:
                # A string from tiles_list to indicate the tile type.
                # And either a Tile object if the tile is present, or None if it isn't.
                wall_item: list[str | Tile | None] = [tiles_list[j], None]
                self.__wall[i][j] = wall_item
            # And then we shift tiles_list one item to the right, modded by the total number of items in tiles_list.
            tiles_list = self._shift_right(tiles_list)

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

        # The consecutive items to the left and right constitute the row score, NOT INCLUDING the tile itself.
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

        # The consecutive items above and below constitute the column score, NOT INCLUDING the tile itself.
        return consecutive_count

    def return_wall(self) -> list[list[list[str | Tile | None]]]:
        """
        Method that iterates through the array and appends each row to a list.

        The list is then returned.
        """

        wall: list[list[list[str | Tile | None]]] = []
        # For each row
        for i in range(self.__rows):
            wall_row: list[list[str | Tile | None]] = []
            for j in range(self.__columns):
                wall_item: list[str | Tile | None] = list(self.__wall[i][j])
                # The item in that row is appended to the row.
                wall_row.append(wall_item)
            # The entire row is appended to the wall.
            wall.append(wall_row)

        # And the entire wall is returned as a list.
        return wall

    def is_tile_on_wall(self, line_index: int, tile_type: str) -> bool:
        """
        Method that takes in the pattern line index and the type of tile, and checks if a corresponding tile exists on the wall.

        If it does, it returns True. Otherwise, it returns False.
        """

        # For the pattern line index selected,
        for wall_row in self.__wall[line_index]:
            # if tile is on corresponding index of the wall
            if wall_row[0] == tile_type:
                # and the value is not None
                if wall_row[1] is not None:
                    # then the tile is on the wall.
                    return True
        # Otherwise, it isn't.
        return False

    def is_row_full(self) -> bool:
        """
        Method that iterates through each of the rows and checks if any of the rows are full.

        If so, it returns True. Otherwise, it returns False.
        """
        # For each row in the wall,
        for row_index in range(self.__rows):
            count: int = 0
            # the nest item is checked to see if it's not None.
            for column_index in range(self.__columns):
                if self.__wall[row_index][column_index][1] is not None:
                    # If so, the count is incremented by 1.
                    count += 1
            # If the consecutive row count is 5, i.e. all tiles are not None, then it's a full row.
            if count == 5:
                # If so, we return True.
                return True
        # Otherwise, we return False.
        return False

    def get_column_index(self, line_index: int, tile_type: str) -> int:
        """
        Method that takes the pattern line index and the type of tile, and retrieves the index of the column.

        It then returns that column index.
        """
        index: int = 0
        # For each associated row in the wall,
        for i, wall_row in enumerate(self.__wall[line_index]):
            # If the associated tile type is the same as the passed in tile type,
            if repr(wall_row[0]) == tile_type:
                # then the index of that tile is returned.
                index = i

        return index

    def place_tile_onto_wall(
        self, row: int, column: int, tile_type: str
    ) -> int:
        """
        Method that takes in the row index and the column index, and places the item onto the wall.

        It then returns the score.
        """
        score: int = 0

        # A new tile is added onto the wall at the selected row and column.
        self.__wall[row][column][1] = Tile(tile_type)

        # The row score is calculated, which counts the number of adjacent items in that row.
        row_score: int = self._count_adjacent_row_items(row, column)
        # Also, the column score is calculated, which counts the number of adjacent items in that column.
        column_score: int = self._count_adjacent_column_items(row, column)

        # consecutive items in the row (excluding item) + consecutive items in the column (excluding item) + item itself for each row and column.
        score = row_score + column_score + 2

        # That score is then returned.
        return score

    def count_full_rows(self) -> int:
        """
        Method that iterates through each of the rows and checks if they're full.

        It returns a count of full rows.
        """
        full_row_count: int = 0

        # For each row in the wall,
        for row_index in range(self.__rows):
            consecutive_count: int = 0
            # the next item is checked to see if it's not None.
            for column_index in range(self.__columns):
                if self.__wall[row_index][column_index][1] is not None:
                    # If so, the count is incremented by 1.
                    consecutive_count += 1
            # If the consecutive row count is 5, i.e. all tiles are not None, then it's a full row.
            if consecutive_count == 5:
                # And the full row count is incremented by 1.
                full_row_count += 1

        # The full row count is then returned.
        return full_row_count

    def count_full_columns(self) -> int:
        """
        Method that iterates through each of the columns and checks if they're full.

        It returns a count of full columns.
        """
        full_column_count: int = 0

        # For each column in the wall,
        for row_index in range(self.__rows):
            consecutive_count: int = 0
            # the next item is checked to see if it's not None.
            for column_index in range(self.__columns):
                if self.__wall[column_index][row_index][1] is not None:
                    # If so, the count is incremented by 1.
                    consecutive_count += 1
            # If the consecutive column count is 5, i.e. all tiles are not None, then it's a full column.
            if consecutive_count == 5:
                # And the full column count is incremented by 1.
                full_column_count += 1

        # The full column count is then returned.
        return full_column_count

    def count_full_tiles(self) -> int:
        """
        Method that iterates through each of the rows and columns diagonally and checks if it has a full row of tiles.

        It returns a count of diagonal tiles.
        """
        full_tile_count: int = 0

        # For each row in the wall,
        for row_index in range(self.__rows):
            consecutive_count: int = 0
            # And for each column,
            for column_index in range(self.__columns):
                # If the row + column % rows of the item is not None
                if (
                    self.__wall[column_index][
                        (row_index + column_index) % self.__rows
                    ][1]
                    is not None
                ):
                    # If so, the count is incremented by 1.
                    consecutive_count += 1
            # If so, the consecutive count is 5, i.e. all tiles are not None. And it's a full diagonal row. (all the tiles of that type are on the wall).
            if consecutive_count == 5:
                full_tile_count += 1

        # The full diagonal row count is then returned.
        return full_tile_count
