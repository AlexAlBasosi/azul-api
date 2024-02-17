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
        self.__start_marker: Tile = Tile("start")
        self.__center_of_table: list[Tile] = [self.__start_marker]
        self.__lid: list[Tile] = []
        self.__board: Board = Board()

    def _add_tiles_to_center(self, tiles: list[Tile]) -> None:
        for tile in tiles:
            self.__lid.append(tile)

    def initalise_factories(self, *, num_of_players: int) -> list[list[Tile]]:
        """
        Method takes in the number of players, and based on that initilialises the factories, takes the correct
        number of tiles from the bag, and then places them into the relevant factories,
        """
        if num_of_players not in (2, 3, 4):
            raise ValueError("Azul is only designed for 2 - 4 players.")

        num_of_factories: int = (
            5 if num_of_players == 2 else 7 if num_of_players == 3 else 9
        )
        tiles_from_bag: list[Tile] = self.__bag.remove_tiles_from_bag(
            num_of_factories
        )

        factories: list[list[Tile]] = self.__factory.add_tiles_to_factories(
            tiles_from_bag
        )

        # TODO: error handling

        return factories

    def return_factories(self) -> list[list[Tile]]:
        """
        Method that returns a list of the Factories and the Tiles contained in each Factory.
        """
        factories = [factory_tiles for factory_tiles in iter(self.__factory)]

        return factories

    def return_center(self) -> list[Tile]:
        """
        Method that returns a list of the Tiles in the center of the table.
        """
        center_of_table = [tile for tile in self.__center_of_table]

        return center_of_table

    def return_lid(self) -> list[Tile]:
        """
        Method that returns a list of the Tiles in the lid.
        """
        lid = [tile for tile in self.__lid]

        return lid

    # Refactor the below
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
        if factory_index not in range(0, 7):
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
            print(value_message)
        except IndexError as index_message:
            print(index_message)
        except TypeError as type_message:
            print(type_message)

        return returned_tiles

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
            print(value_message)
        except IndexError as index_message:
            print(index_message)
        except OverflowError as overflow_message:
            print(overflow_message)

    # TODO: Refactor above methods to play_turn_factory and play_turn_center, which call the above methods.
    def play_turn_factory(self, *, tiles: list[Tile]) -> None:
        ...
    # TODO: Add method to add_to_floor_line
    def place_onto_floor_line(self, *, tiles: list[Tile]) -> list[Tile] | None:
        return self.__board.place_tiles_onto_floor_line(tiles=tiles)