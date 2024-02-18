from .board import Board
from .bag import Bag
from .tile import Tile
from .factory import Factory


class Game:
    """
    Facade class responsible for exposing access to all the various components of the game.

    This is the only class that will be accessed by users of the game.
    """

    __bag: Bag
    __factory: Factory
    __num_of_factories: int
    __center_of_table: list[Tile]
    __lid: list[Tile]
    __start_marker: Tile
    __board: Board

    def __init__(self) -> None:
        """
        Constructor method that initliases Bag object.
        """
        self.__bag = Bag()
        self.__factory: Factory = Factory()
        self.__num_of_factories: int = 0
        self.__start_marker: Tile = Tile("start")
        self.__center_of_table: list[Tile] = [self.__start_marker]
        self.__lid: list[Tile] = []
        self.__board: Board = Board()

    def _add_tiles_to_center(self, tiles: list[Tile]) -> None:
        for tile in tiles:
            self.__center_of_table.append(tile)

    def initalise_factories(self, *, num_of_players: int) -> list[list[Tile]]:
        """
        Method takes in the number of players, and based on that initilialises the factories, takes the correct
        number of tiles from the bag, and then places them into the relevant factories,
        """
        if num_of_players not in (2, 3, 4):
            raise ValueError("Azul is only designed for 2 - 4 players.")

        self.__num_of_factories: int = (
            5 if num_of_players == 2 else 7 if num_of_players == 3 else 9
        )

        try:
            tiles_from_bag: list[Tile] = self.__bag.remove_tiles_from_bag(
                self.__num_of_factories
            )

            factories: list[list[Tile]] = self.__factory.add_tiles_to_factories(
                tiles_from_bag
            )

        except ValueError as value_message:
            raise ValueError(value_message) from value_message

        return factories

    def return_factories(self) -> list[list[Tile]]:
        """
        Method that returns a list of the Factories and the Tiles contained in each Factory.
        """
        factories: list[list[Tile]] = [factory_tiles for factory_tiles in iter(self.__factory)]

        return factories

    def return_center(self) -> list[Tile | str]:
        """
        Method that returns a list of the Tiles in the center of the table.
        """
        center_of_table: list[Tile | str] = []
        for tile in self.__center_of_table:
            if tile == "start":
                center_of_table.append("start")
            else:
                center_of_table.append(tile)

        return center_of_table

    def return_lid(self) -> list[str]:
        """
        Method that returns a list of the Tiles in the lid.
        """
        lid = [tile.getattr() for tile in self.__lid]

        return lid
    
    def return_pattern_lines(self) -> list[list[Tile]]:
        """
        Method that returns a list of the pattern lines and the tiles within them.
        """
        return self.__board.return_pattern_lines()
    
    def return_floor_line(self) -> list[str]:
        """
        Method that returns a list of the floor line tiles.
        """
        return self.__board.return_floor_line()
    
    def return_wall(self) -> list[dict[str, Tile]]:
        """
        Method that iterates through the array and appends each row to a list.

        The list is then returned.
        """
        return self.__board.return_wall()

    def select_from_factory(
        self, *, tile_type: str, factory_index: int
    ) -> list[list[Tile]]:
        """
        Method that takes in the type of tiles to be taken from the factory, as well as the index of the factory to take the tiles from.

        It removes the tiles from the specified factory, and returns a list of selected and discarded tiles.
        """

        # Validation to ensure that the type being passed in is of the specified types.
        if tile_type not in ("black", "ice", "blue", "yellow", "red"):
            raise ValueError(
                "Tile type must be a string that contains either 'black', 'ice', 'blue', 'yellow', or 'red'."
            )
        # Validation to ensure that an index isn't passed in for a factory that doesn't exist.
        if factory_index not in range(0, self.__num_of_factories):
            raise IndexError(
                "You can only select a factory index with an integer from 0-3, as it only contains up to four tiles."
            )

        returned_tiles: list[list[Tile]] = []

        try:
            # A method is called on the factory object to remove all tiles of type from specified factory.
            # Which returns lists of selected and discarded tiles.
            returned_tiles = self.__factory.remove_all_instances_of_tile(
                tile_type=tile_type, factory_index=factory_index
            )

        # The errors raised are handled here, which are printed onto the console. In a production environment these would be added to a logger.
        except ValueError as value_message:
            raise ValueError(value_message) from value_message
        except IndexError as index_message:
            raise IndexError(index_message) from index_message
        except TypeError as type_message:
            raise TypeError(type_message) from type_message

        return returned_tiles
    
    def select_from_center(self, *, tile_type: str) -> list[Tile]:
        """
        Method that takes the type of tile to be taken from the center of the table, and removes all tiles from the center.

        It then returned the removed tiles as a list.
        """
        if tile_type not in self.__center_of_table:
            raise IndexError("No Tile of this type found within the factory!")
        if not isinstance(tile_type, str):
            raise TypeError("tile_type should be a string!")
        
        selected_tiles: list[Tile] = []
        for tile in self.__center_of_table:
            if tile == tile_type:
                selected_tiles.append(tile)
                self.__center_of_table.remove(tile)

        return selected_tiles
    
    def place_onto_pattern_line(
        self,
        *,
        tile_type: str,
        returned_tiles: list[list[Tile]],
        line_index: int
    ) -> None:
        """
        Method that takes the type of tiles to be placed onto the pattern line, as well as the index of the pattern line to place the tiles onto.

        It then places the selected tiles onto the specified pattern line, and adds the discarded tiles to the center of the table.
        """
        # Validation to ensure that the type being passed in is of the specified types.
        if tile_type not in ("black", "ice", "blue", "yellow", "red"):
            raise ValueError(
                "Tile type must be a string that contains either 'black', 'ice', 'blue', 'yellow', or 'red'."
            )
        # Validation that ensures an index isn't passed in for a pattern line that doesn't exist.
        if line_index not in range(0, 5):
            raise IndexError(
                "Selected Pattern Line doesn't exist. Please provide an index from 0-4."
            )
        if len(returned_tiles) <= 0:
            raise IndexError("Tile list provided is empty!")

        try:
            selected_tiles: list[Tile] = returned_tiles[0]
            discarded_tiles: list[Tile] = returned_tiles[1]

            #TODO: Add logic to check whether a corresponding tile exists on the wall.

            # The selected tiles are placed onto the specified pattern line.
            self.__board.place_tile_onto_pattern_line(
                selected_tiles, tile_type, line_index
            )

            # The discarded tiles are added to the lid.
            self._add_tiles_to_center(discarded_tiles)

        # The errors raised are handled here, which are printed onto the console. In a production environment these would be added to a logger.
        except ValueError as value_message:
            raise ValueError(value_message) from value_message
        except IndexError as index_message:
            raise IndexError(index_message) from index_message
        except OverflowError as overflow_message:
            raise OverflowError(overflow_message) from overflow_message

    def place_onto_floor_line(self, *, tiles: list[Tile]) -> None:
        """
        Method that takes in a list of tiles to be added to the floor line. If there is space remaining on the floor line, it will be added.

        Otherwise, the remaining tiles will be added to the lid.
        """
        for tile in tiles:
            if tile not in ("black", "ice", "blue", "yellow", "red", "start"):
                raise ValueError("Tile type must be a string that contains either 'black', 'ice', 'blue', 'yellow', 'red', or 'start'.")
        if len(tiles) <= 0:
                raise IndexError("List provided is empty!")
        try:
            returned_tiles: list[Tile] | None = self.__board.place_tiles_onto_floor_line(tiles=tiles)
            if(returned_tiles is not None):
                for tile in returned_tiles:
                    self.__lid.append(tile)

        except ValueError as value_message:
            raise ValueError(value_message) from value_message
        except IndexError as index_message:
            raise IndexError(index_message) from index_message
            