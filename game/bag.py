"""
Module containing the Bag class implementation.
"""

from random import randrange
from typing import Any
from collections.abc import Iterator, Mapping
from .tile import Tile
from .rule_error import RuleError


class Bag:
    """
    Factory class responsible for the creation of Tiles.
    """

    __tile_set: set[str] = {"black", "ice", "blue", "yellow", "red"}
    __tile_bag: dict[Tile, int] = {}

    def __init__(self: Any) -> None:
        """
        Constructor method that iterates through each tile type in the tile set and adds 20 to the tile bag.

        This populates the tile bag with 20 tiles of each type.
        """

        for tile in self.__tile_set:
            self.__tile_bag[tile] = 20

    def __iter__(self: Any) -> Iterator[dict[Tile, int]]:
        """
        Iterator that loops through the bag, and for each item returns a 'count' number of tiles.
        """
        tiles = self.__tile_bag
        for item, count in tiles.items():
            for _ in range(count):
                yield item

    def _list_to_mapping(self, tiles: list[Tile]) -> Mapping[Tile, int]:
        """
        This method takes a list and converts it to a mapping of Tile -> int.
        """
        tile_mapping: dict[Tile, int] = {}
        # For each tile in tile list,
        for tile in tiles:
            tile_count: int = 0
            # count each occurence of the tile,
            for _, current_tile in enumerate(tiles):
                if current_tile == tile:
                    # increment the count of that tile
                    tile_count += 1
            # and then add the count to the tile_mapping with the tile as a key.
            tile_mapping[tile] = tile_count

        return tile_mapping

    def _update(self, new_tile_counts: Mapping[Tile, int]) -> None:
        """
        Update method that provides a Mapping of tiles and their count to be updated.
        """
        tiles = self.__tile_bag
        for (
            tile,
            count,
        ) in new_tile_counts.items():  # It loops through the Mapping provided
            new_count = (
                tiles.get(tile, 0) + count
            )  # If the tile already exists, it'll add the new count to it, otherwise it's set to 0
            if new_count > 0:
                tiles[
                    tile
                ] = new_count  # Updates the bag with the new tile count
            elif (
                tile in tiles
            ):  # Otherwise if the count is negative, it will remove that many items from the bag.
                del tiles[tile]

    def _remove(self, *tiles_to_remove: Tile) -> None:
        """
        Remove method that provides Tile to be removed, and calls the _update method to remove it.
        """
        remove_tile_counts: dict[Tile, int] = {}
        # For each tile to remove,
        for tile in tiles_to_remove:
            # Get the current count and subtract it by 1.
            remove_tile_counts[tile] = remove_tile_counts.get(tile, 0) - 1
        # Then update it with the new count.
        self._update(remove_tile_counts)

    def __len__(self) -> int:
        return sum(self.__tile_bag.values())

    def return_tile_bag(self) -> list[Tile]:
        """
        Method that returns the tiles in the bag as a list.
        """
        # For each tile in the tile bag, it's added to a list and returned.
        tiles_list: list[Tile] = [tile for tile in self.__tile_bag]
        return tiles_list

    def remove_tiles_from_bag(self, num_of_factories: int) -> list[Tile]:
        """
        This method takes in the number of Factories, and randomly removes 4 * the number of Factories and returns them.

        For example, if there are 5 factories, 20 random tiles are removed from the bag and returned.
        """
        # Validation to ensure the number of factories is 5, 7, or 9.
        # Otherwise it throws a RuleError.
        if num_of_factories not in (5, 7, 9):
            raise RuleError(
                {
                    "class": "Bag",
                    "method": "remove_tiles_from_bag",
                    "message": "You can only have 5, 7, or 9 factories! Please check the Azul rulebook for guidance.",
                }
            )

        tiles_to_remove: list[Tile] = []
        tiles_list: list[Tile] = [
            tile for tile in self.__tile_bag
        ]  # A list is created of all the colours of the tile that exists in the bag.

        if not tiles_list:
            return []

        for _ in range(0, num_of_factories * 4):  # For each Factory times 4...
            tiles_to_remove.append(
                tiles_list[randrange(0, len(tiles_list))]
            )  # ...a random number is generated, and the tile at
            # that index is appended to the list.

        for (
            tile
        ) in (
            tiles_to_remove
        ):  # Then for each tile in that list, it's removed from the bag.
            self._remove(tile)

        return list(
            tiles_to_remove
        )  # And the whole list is returned, in chunks of 4.

    def add_tiles_to_bag(self, tiles: list[Tile]) -> None:
        """
        Method that takes a list of tiles to be added to the bag, and adds them to the bag.
        """
        # Convert the list of tiles to be added to a mapping,
        mapped_tiles: Mapping[Tile, int] = self._list_to_mapping(tiles)
        # then update it with the mapped tiles.
        self._update(mapped_tiles)
