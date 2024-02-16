from .pattern_line import PatternLine

class Board:
    """
    The Board class follows the Facade pattern, handling instantiation and methods associated with its sub-components.
    """

    __pattern_lines: PatternLine

    def __init__(self) -> None:
        self.__pattern_lines = PatternLine()