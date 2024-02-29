"""
Module containing the Game class implementation.
"""

from .board import Board
from .bag import Bag
from .tile import Tile
from .factory import Factory
from .rule_error import RuleError

class Game:
    """
    Facade class responsible for exposing access to all the various components of the game.

    This is the only class that will be accessed by users of the game.
    """

    __bag: Bag
    __factory: Factory
    __num_of_players: int
    __num_of_factories: int
    __center_of_table: list[Tile]
    __lid: list[Tile]
    __start_marker: Tile
    __boards: list[Board]
    __final_scores: list[int]

    def __init__(self) -> None:
        """
        Constructor method that initliases Bag object.
        """
        self.__bag = Bag()
        self.__factory: Factory = Factory()
        self.__num_of_players: int = 0
        self.__num_of_factories: int = 0
        self.__start_marker: Tile = Tile("start")
        self.__center_of_table: list[Tile] = [self.__start_marker]
        self.__lid: list[Tile] = []
        self.__boards: list[Board] = []
        self.__final_scores: list[int] = []

    def _add_tiles_to_center(self, tiles: list[Tile]) -> None:
        for tile in tiles:
            self.__center_of_table.append(tile)

    def _is_in_board_floor_lines(self, tile: Tile) -> bool:
        for board in self.__boards:
            if tile in board.return_floor_line():
                return True
        return False

    def return_num_of_factories(self) -> int:
        """
        Method that returns the number of factories.
        """

        return self.__num_of_factories

    def return_num_of_players(self) -> int:
        """
        Method that returns the number of players.
        """

        return self.__num_of_players

    def is_factories_empty(self) -> bool:
        """
        Method that returns whether the factories are empty.

        Returns True if they're empty. Returns False otherwise.
        """

        return self.__factory.is_factories_empty()

    def is_center_empty(self) -> bool:
        """
        Method that checks if the center is empty.

        Returns True if empty. Returns False otherwise.
        """

        return not len(self.__center_of_table) > 0

    def is_pattern_line_empty(
        self, *, line_index: int, player_index: int
    ) -> bool:
        """
        Method that checks if selected pattern line on a particular board is empty.

        Returns True if empty. Returns False otherwise.
        """
        return not self.__boards[player_index].is_pattern_line_full(
            line_index=line_index
        )

    def initialise_players(self, *, num_of_players: int) -> list[int]:
        """
        Method that takes in the number of players, and initialises the boards.

        It then returns a list of the player indices.
        """
        if num_of_players not in (2, 3, 4):
            raise RuleError({
                "class": "Game",
                "method": "initialise_players",
                "message": "Azul is only designed for 2 - 4 players."
            })

        self.__num_of_players = num_of_players

        player_indexes: list[int] = []
        for player_index in range(num_of_players):
            player_indexes.append(player_index)
            self.__boards.append(Board())

        return player_indexes

    def initalise_factories(self) -> list[list[Tile]]:
        """
        Method takes in the number of players, and based on that initilialises the factories, takes the correct
        number of tiles from the bag, and then places them into the relevant factories,
        """

        self.__num_of_factories: int = (
            5
            if self.__num_of_players == 2
            else 7
            if self.__num_of_players == 3
            else 9
        )

        bag_tiles: list[Tile] = self.__bag.return_tile_bag()
        if len(bag_tiles) < (self.__num_of_factories * 4):
            self.__bag.add_tiles_to_bag(self.__lid)
            self.__lid.clear()

        tiles_from_bag: list[Tile] = self.__bag.remove_tiles_from_bag(
            self.__num_of_factories
        )

        # If the lid is empty, take the current contents of the factories and add them to the bag.
        current_factories: list[Tile] = []
        for factory in self.return_factories():
            for factory_tile in factory:
                current_factories.append(factory_tile)

        if not self.__lid:
            self.__bag.add_tiles_to_bag(current_factories)

        self.__factory.clear_factories()

        factories: list[list[Tile]] = self.__factory.add_tiles_to_factories(
            tiles_from_bag
        )

        return factories

    def return_factories(self) -> list[list[Tile]]:
        """
        Method that returns a list of the Factories and the Tiles contained in each Factory.
        """
        factories: list[list[Tile]] = [
            factory_tiles for factory_tiles in iter(self.__factory)
        ]

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

    def return_lid(self) -> list[Tile]:
        """
        Method that returns a list of the Tiles in the lid.
        """
        lid = [tile for tile in self.__lid]

        return lid

    def return_pattern_lines(self, *, player_index: int) -> list[list[Tile]]:
        """
        Method that returns a list of the pattern lines and the tiles within them.
        """
        return self.__boards[player_index].return_pattern_lines()

    def return_floor_line(self, *, player_index: int) -> list[str | Tile]:
        """
        Method that returns a list of the floor line tiles.
        """
        return self.__boards[player_index].return_floor_line()

    def return_wall(
        self, *, player_index: int
    ) -> list[list[list[str | Tile | None]]]:
        """
        Method that iterates through the array and appends each row to a list.

        The list is then returned.
        """
        return self.__boards[player_index].return_wall()

    def is_tile_on_wall(
        self, *, line_index: int, tile_type: str, player_index: int
    ) -> bool:
        """
        Method that takes the line index, tile type, and player index, and checks if there is a tile on the corresponding row on the wall with the same colour.

        Returns True if so. Returns False otherwise.
        """
        return self.__boards[player_index].is_tile_on_wall(
            line_index, tile_type
        )

    def return_score(self, *, player_index: int) -> int:
        """
        Method that takes the player index.

        It then returns the score.
        """
        return self.__boards[player_index].return_score()

    def select_from_factory(
        self, *, tile_type: str, factory_index: int
    ) -> list[list[Tile]]:
        """
        Method that takes in the type of tiles to be taken from the factory, as well as the index of the factory to take the tiles from.

        It removes the tiles from the specified factory, and returns a list of selected and discarded tiles.
        """

        # Validation to ensure that the type being passed in is of the specified types.
        if tile_type not in ("black", "ice", "blue", "yellow", "red"):
            raise ValueError({
                "class": "Game",
                "method": "select_from_factory",
                "message": "Tile type must be a string that contains either 'black', 'ice', 'blue', 'yellow', or 'red'."
            })
        # Validation to ensure that an index isn't passed in for a factory that doesn't exist.
        if factory_index not in range(0, self.__num_of_factories):
            raise IndexError({
                "class": "Game",
                "method": "select_from_factory",
                "message": "You can only select a factory index with an integer from 0-3, as it only contains up to four tiles."
            })

        returned_tiles: list[list[Tile]] = []

        # A method is called on the factory object to remove all tiles of type from specified factory.
        # Which returns lists of selected and discarded tiles.
        returned_tiles = self.__factory.remove_all_instances_of_tile(
            tile_type=tile_type, factory_index=factory_index
        )

        return returned_tiles

    def select_from_center(
        self, *, tile_type: str, player_index: int
    ) -> list[Tile]:
        """
        Method that takes the type of tile to be taken from the center of the table, and removes all tiles from the center.

        It then returned the removed tiles as a list.
        """

        # If requested tile isn't in the center or the table, there are no tiles in the center, or tile is not a string, it will throw an error.
        if tile_type not in self.__center_of_table:
            raise IndexError({
                "class": "Game",
                "method": "select_from_center",
                "message": "No Tile of this type found within the center!"
            })
        if len(self.__center_of_table) <= 0:
            raise IndexError({
                "class": "Game",
                "method": "select_from_center",
                "message": "There are no tiles in the center of the table!"
            })
        if not isinstance(tile_type, str):
            raise TypeError({
                "class": "Game",
                "method": "select_from_center",
                "message": "tile_type should be a string!"
            })

        # For each tile in the center of the table, it will append it to the selected tiles, and then remove it from the center of the table.
        selected_tiles: list[Tile] = []
        for tile in self.__center_of_table:
            if tile == tile_type:
                selected_tiles.append(tile)
                self.__center_of_table.remove(tile)

        # If the user selects from the center, it will add the start marker to their floor line, and remove it from the center of the table.
        if not self._is_in_board_floor_lines(self.__start_marker):
            self.__boards[player_index].place_tiles_onto_floor_line(
                tiles=[self.__start_marker]
            )
        if self.__start_marker in self.__center_of_table:
            self.__center_of_table.remove(self.__start_marker)

        return selected_tiles

    def place_onto_pattern_line(
        self,
        *,
        tile_type: str,
        returned_tiles: list[list[Tile]],
        player_index: int,
        line_index: int
    ) -> None:
        """
        Method that takes the type of tiles to be placed onto the pattern line, as well as the index of the pattern line to place the tiles onto.

        It then places the selected tiles onto the specified pattern line, and adds the discarded tiles to the center of the table.
        """
        # Validation to ensure that the type being passed in is of the specified types.
        if tile_type not in ("black", "ice", "blue", "yellow", "red"):
            raise ValueError({
                "class": "Game",
                "method": "place_onto_pattern_line",
                "message": "Tile type must be a string that contains either 'black', 'ice', 'blue', 'yellow', or 'red'."
            })
        # Validation that ensures an index isn't passed in for a pattern line that doesn't exist.
        if line_index not in range(0, 5):
            raise IndexError({
                "class": "Game",
                "method": "place_onto_pattern_line",
                "message": "Selected Pattern Line doesn't exist. Please provide an index from 0-4."
            })
        if len(returned_tiles) <= 0:
            raise IndexError({
                "class": "Game",
                "method": "place_onto_pattern_line",
                "message": "Tile list provided is empty!"
            })

        selected_tiles: list[Tile] = returned_tiles[0]
        discarded_tiles: list[Tile] = returned_tiles[1]

        # If tile already exists at the line index on the wall, an error is raised.
        if self.__boards[player_index].is_tile_on_wall(line_index, tile_type):
            raise RuleError({
                "class": "Game",
                "method": "place_onto_pattern_line",
                "message": "Tile already exists on the wall! Cannot add to this pattern line."
            })

        # The selected tiles are placed onto the specified pattern line.
        self.__boards[player_index].place_tile_onto_pattern_line(
            selected_tiles, tile_type, line_index
        )

        # The discarded tiles are added to the center of the table.
        self._add_tiles_to_center(discarded_tiles)

    def place_onto_floor_line(
        self, *, tiles: list[Tile], player_index: int
    ) -> None:
        """
        Method that takes in a list of tiles to be added to the floor line. If there is space remaining on the floor line, it will be added.

        Otherwise, the remaining tiles will be added to the lid.
        """
        for tile in tiles:
            if tile not in ("black", "ice", "blue", "yellow", "red", "start"):
                raise ValueError({
                    "class": "Game",
                    "method": "place_onto_floor_line",
                    "message": "Tile type must be a string that contains either 'black', 'ice', 'blue', 'yellow', 'red', or 'start'."
                })
        if len(tiles) <= 0:
            raise IndexError({
                "class": "Game",
                "method": "place_onto_floor_line",
                "message": "List provided is empty!"              
            })

        returned_tiles: list[Tile] | None = self.__boards[
            player_index
        ].place_tiles_onto_floor_line(tiles=tiles)
        if returned_tiles is not None:
            for tile in returned_tiles:
                self.__lid.append(tile)

    def place_onto_wall(self, *, player_index: int) -> None:
        """
        Method that takes the line index and player index, and places the tile onto the wall.

        It then stores the list of tiles from the cleared pattern lines into the lid.
        """
        if len(self.__center_of_table) > 0:
            raise RuleError({
                "class": "Game",
                "method": "place_onto_wall",
                "message": "Cannot place onto the wall while the center still has tiles!"
            })
        if not self.__factory.is_factories_empty():
            raise RuleError({
                "class": "Game",
                "method": "place_onto_wall",
                "message": "Cannot place onto the wall while the factories still have tiles!"
            })

        returned_tiles: list[list[Tile]] = self.__boards[
            player_index
        ].place_tiles_onto_wall()

        for cleared_line in returned_tiles:
            if len(cleared_line) > 0:
                self.__lid += cleared_line

    def _calculate_final_score(self, player_index: int) -> int:
        """
        Method that takes the player index and adds the final scores to the player's score.

        It then returns that score.
        """
        self.__boards[player_index].add_final_scores()

        return self.__boards[player_index].return_score()

    def calculate_final_scores(self) -> list[int]:
        """
        Method that iterates through the number of players, and then adds them to the final scores.

        It then returns the final scores.
        """
        final_scores: list[int] = [
            self._calculate_final_score(player_index=player_index)
            for player_index in range(self.__num_of_players)
        ]

        self.__final_scores += final_scores
        return final_scores

    def is_game_ended(self) -> bool:
        """
        Method that checks whether the game has ended.

        If so, it returns True. Otherwise, it returns False.
        """
        for player in range(self.__num_of_players):
            if self.__boards[player].is_wall_row_full():
                return True
        return False

    def return_winners(self) -> dict[int, int]:
        """
        Method that iterates through the final scores, and returns a dictionary of the winner indexes and their corresponding score.
        """
        player_scores: list[int] = self.__final_scores

        if not player_scores:
            return {}

        max_score = max(player_scores)
        max_indexes = [
            index
            for index, score in enumerate(player_scores)
            if score == max_score
        ]

        return {index: max_score for index in max_indexes}
