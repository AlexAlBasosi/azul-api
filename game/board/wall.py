import numpy as np
from ..tile import Tile


class Wall:
    """
    The Wall class handles methods associated with adding and removing tiles from the floor line.
    """

    __rows: int = 5
    __wall = np.empty((__rows), dtype=object)

    def __init__(self) -> None:
        self.__wall = np.empty((self.__rows), dtype=object)

        self.__wall[0] = {
            "blue": None,
            "yellow": None,
            "red": None,
            "black": None,
            "ice": None,
        }
        self.__wall[1] = {
            "ice": None,
            "blue": None,
            "yellow": None,
            "red": None,
            "black": None,
        }
        self.__wall[2] = {
            "black": None,
            "ice": None,
            "blue": None,
            "yellow": None,
            "red": None,
        }
        self.__wall[3] = {
            "red": None,
            "black": None,
            "ice": None,
            "blue": None,
            "yellow": None,
        }
        self.__wall[4] = {
            "yellow": None,
            "red": None,
            "black": None,
            "ice": None,
            "blue": None,
        }

    def return_wall(self) -> list[dict[str, Tile]]:
        """
        Method that iterates through the array and appends each row to a list.

        The list is then returned.
        """
        wall: list[dict[str, Tile]] = []
        for index in range(self.__rows):
            wall.append(self.__wall[index])
        return wall
