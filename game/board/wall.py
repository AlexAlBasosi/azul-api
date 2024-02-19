import numpy as np
from ..tile import Tile


class Wall:
    """
    The Wall class handles methods associated with adding and removing tiles from the floor line.
    """

    __rows: int = 5
    __wall = np.empty((__rows), dtype=object)

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
        self.__wall = np.empty((self.__rows), dtype=object)

        tiles_list: list[str | None] = ['blue', 'yellow', 'red', 'black', 'ice']
        for index, _ in enumerate(tiles_list):
            self.__wall[index] = {
                tiles_list[0]: None,
                tiles_list[1]: None,
                tiles_list[2]: None,
                tiles_list[3]: None,
                tiles_list[4]: None
            }

            tiles_list = self._shift_right(tiles_list)

    def return_wall(self) -> list[dict[str, Tile]]:
        """
        Method that iterates through the array and appends each row to a list.

        The list is then returned.
        """
        wall: list[dict[str, Tile]] = []
        for index in range(self.__rows):
            wall.append(self.__wall[index])
        return wall
