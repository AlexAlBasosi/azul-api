from .tile import Tile
from typing import Generator
from collections.abc import Iterator


class Factory:
    """
    Class that implements the addition and removal of Tiles from Factories.
    """

    __factories: list[list[Tile]]

    def __init__(self) -> None:
        self.__factories = []

    def __iter__(self) -> Iterator[list[Tile]]:
        for factory_tiles in self.__factories:
            yield factory_tiles

    def _chunks(
        self, tile_list: list[Tile], chunk_length: int
    ) -> Generator[list[Tile], None, None]:
        """
        Generator function that takes a list of Tiles and splits it into chunks of length 'chunk_length'
        """
        for index in range(0, len(tile_list), chunk_length):
            yield tile_list[index : index + chunk_length]

    def add_tiles_to_factories(
        self, tiles_to_add: list[Tile]
    ) -> list[list[Tile]]:
        """
        Method that takes in the tiles to add to the factories, splits the list into chunks of 4, and adds each chunk to a
        factory.

        Finally, it returns the result back to the game user.
        """
        factories: list[list[Tile]] = list(self._chunks(tiles_to_add, 4))
        for tiles in factories:
            self.__factories.append(tiles)

        return factories

    def remove_all_instances_of_tile(
        self, *, tile_type: str, factory_index: int
    ) -> list[list[Tile]]:
        """
        Method which takes in the type of Tile(s) to remove from the Factory (i.e. red, blue, etc.), as well the index of the Factory the user is
        selecting the Tiles from.

        Then returns a list of the selected tiles and discarded tiles.
        """

        # Validation ensures that the user is selecting a tile that exists in the factory, as well as whether the values passed in for
        # tile_type and factory_index are a string and integer, respectively.
        if tile_type not in self.__factories[factory_index]:
            raise IndexError("No Tile of this type found within the factory!")
        if not isinstance(tile_type, str):
            raise TypeError("tile_type should be a string!")
        if not isinstance(factory_index, int):
            raise TypeError("factory_index should be an integer!")

        selected_tiles: list[Tile] = []
        discarded_tiles: list[Tile] = []

        # For each Tile in the selected Factory, if the Tile is NOT the type selected, it will be appended to the discarded_tiles list,
        # otherwise, it's appended to the selected_tiles list.
        for tile in self.__factories[factory_index]:
            if tile != tile_type:
                discarded_tiles.append(tile)
            else:
                selected_tiles.append(tile)

        # Replace tiles in factory at index factory_index with an empty list, thus removing the elements.
        self.__factories[factory_index] = []

        return [selected_tiles, discarded_tiles]

    def is_factories_empty(self) -> bool:
        """
        Method that checks whether the factories are empty.

        If so, it returns True. Otherwise, if any of the factories are not empty, it will return False.
        """
        for factory in self.__factories:
            if len(factory) > 0:
                return False
        return True