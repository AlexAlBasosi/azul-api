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
        self.__center_of_table: list[Tile] = []
        self.__lid: list[Tile] = []
        self.__start_marker: Tile = Tile("start")
        self.__board: Board = Board()

    
    def initalise_factories(self, *, num_of_players: int) -> list[list[Tile]]:
        """
        Method takes in the number of players, and based on that initilialises the factories, takes the correct
        number of tiles from the bag, and then places them into the relevant factories,
        """
        if num_of_players not in (2, 3, 4):
            raise ValueError("Azul is only designed for 2 - 4 players.")
        
        num_of_factories: int = 5 if num_of_players == 2 else 7 if num_of_players == 3 else 9
        tiles_from_bag: list[Tile] = self.__bag.remove_tiles_from_bag(num_of_factories)

        factories: list[list[Tile]] = self.__factory.add_tiles_to_factories(tiles_from_bag)

        #TODO: error handling

        return factories
    
    #TODO: Include method to show the tiles in the existing factories
    def return_factories(self) -> list[list[Tile]]:
        factories = [
            factory_tiles
            for factory_tiles in iter(self.__factory)
        ]

        return factories

    #TODO: Include method to show the tiles in the center of the table

    
    # Refactor the below
    def test(self) -> None:
        print(self.__factory.remove_all_instances_of_tile(tile_type="red", factory_index=0))
    