from collections import deque
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
            pattern_line: deque[Tile] = deque(maxlen = line_length)
            self.__pattern_lines.append(pattern_line)
        print(self.__pattern_lines)