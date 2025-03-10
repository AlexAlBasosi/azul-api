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
        # Add the selected tile list to the center of the table.
        for tile in tiles:
            self.__center_of_table.append(tile)

    def _is_in_board_floor_lines(self, tile: Tile) -> bool:
        for board in self.__boards:
            if tile in board.return_floor_line():
                return True
        return False

    def _calculate_final_score(self, player_index: int) -> int:
        """
        Method that takes the player index and adds the final scores to the player's score.

        It then returns that score.
        """
        # The final scores are added.
        self.__boards[player_index].add_final_scores()

        # And then returned.
        return self.__boards[player_index].return_score()

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

    def return_factories(self) -> list[list[Tile]]:
        """
        Method that returns a list of the Factories and the Tiles contained in each Factory.
        """
        # Each factory in the factories are iterated over and returned as a list of lists.
        factories: list[list[Tile]] = [
            factory_tiles for factory_tiles in iter(self.__factory)
        ]

        return factories

    def return_center(self) -> list[Tile | str]:
        """
        Method that returns a list of the Tiles in the center of the table.
        """
        center_of_table: list[Tile | str] = []
        # For each tile in the center of the table,
        for tile in self.__center_of_table:
            # If the tile type is "start", append that to the list.
            if tile == "start":
                center_of_table.append("start")
            # Otherwise, append the tile itself.
            else:
                center_of_table.append(tile)
        # The center is returned as a list of lists.
        return center_of_table

    def return_lid(self) -> list[Tile]:
        """
        Method that returns a list of the Tiles in the lid.
        """
        # For each tile in the lid, it's added to a list and returned.
        lid = [tile for tile in self.__lid]

        return lid

    def return_pattern_lines(self, *, player_index: int) -> list[list[Tile]]:
        """
        Method that returns a list of the pattern lines and the tiles within them.
        """
        # Validation to ensure the player_index is valid.
        if player_index not in range(self.__num_of_players):
            raise IndexError(
                {
                    "class": "Game",
                    "method": "return_pattern_lines",
                    "message": f"Please enter a 'player_index' between 0 and {self.__num_of_players - 1}",
                }
            )
        # For the selected player, their pattern lines are returned.
        return self.__boards[player_index].return_pattern_lines()

    def return_floor_line(self, *, player_index: int) -> list[str | Tile]:
        """
        Method that returns a list of the floor line tiles.
        """
        # The floor line is returned.
        return self.__boards[player_index].return_floor_line()

    def return_wall(
        self, *, player_index: int
    ) -> list[list[list[str | Tile | None]]]:
        """
        Method that iterates through the array and appends each row to a list.

        The list is then returned.
        """
        if player_index not in range(self.__num_of_players):
            raise IndexError(
                {
                    "class": "Game",
                    "method": "return_wall",
                    "message": f"Please enter a 'player_index' between 0 and {self.__num_of_players - 1}",
                }
            )
        # For the selected player, their wall is returned.
        return self.__boards[player_index].return_wall()

    def return_score(self, *, player_index: int) -> int:
        """
        Method that takes the player index.

        It then returns the score.
        """
        # Validation to ensure the player_index is valid.
        if player_index not in range(self.__num_of_players):
            raise IndexError(
                {
                    "class": "Game",
                    "method": "return_score",
                    "message": f"Please enter a 'player_index' between 0 and {self.__num_of_players - 1}",
                }
            )

        # For the selected player, their score is returned.
        return self.__boards[player_index].return_score()

    def return_winners(self) -> dict[int, int]:
        """
        Method that iterates through the final scores, and returns a dictionary of the winner indexes and their corresponding score.
        """
        player_scores: list[int] = self.__final_scores

        if not player_scores:
            return {}

        # Max score of all scores is calculated.
        max_score = max(player_scores)
        # For each index in player scores, if it's equal to max score it's added to a list.
        max_indexes = [
            index
            for index, score in enumerate(player_scores)
            if score == max_score
        ]

        # A dict is returned of all the player_indexes whose score is the final score.
        # I.e. if there is more than one winner, all of players and their scores are returned.
        return {index: max_score for index in max_indexes}

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

        return len(self.__center_of_table) <= 0

    def is_pattern_line_empty(
        self, *, line_index: int, player_index: int
    ) -> bool:
        """
        Method that checks if selected pattern line on a particular board is empty.

        Returns True if empty. Returns False otherwise.
        """
        if line_index not in range(5):
            raise IndexError(
                {
                    "class": "Game",
                    "method": "is_pattern_line_empty",
                    "message": "Please enter a 'line_index' between 0 and 5.",
                }
            )

        if player_index not in range(self.__num_of_players):
            raise IndexError(
                {
                    "class": "Game",
                    "method": "is_pattern_line_empty",
                    "message": f"Please enter a 'player_index' between 0 and {self.__num_of_players - 1}",
                }
            )
        return not self.__boards[player_index].is_pattern_line_full(
            line_index=line_index
        )

    def is_tile_on_wall(
        self, *, line_index: int, tile_type: str, player_index: int
    ) -> bool:
        """
        Method that takes the line index, tile type, and player index, and checks if there is a tile on the corresponding row on the wall with the same colour.

        Returns True if so. Returns False otherwise.
        """
        if line_index not in range(5):
            raise IndexError(
                {
                    "class": "Game",
                    "method": "is_tile_on_wall",
                    "message": "Please enter a 'line_index' between 0 and 5.",
                }
            )
        if not isinstance(tile_type, str):
            raise TypeError(
                {
                    "class": "Game",
                    "method": "is_tile_on_wall",
                    "message": "tile_type should be a string!",
                }
            )

        if player_index not in range(self.__num_of_players):
            raise IndexError(
                {
                    "class": "Game",
                    "method": "is_tile_on_wall",
                    "message": f"Please enter a 'player_index' between 0 and {self.__num_of_players - 1}",
                }
            )

        return self.__boards[player_index].is_tile_on_wall(
            line_index, tile_type
        )

    def is_game_ended(self) -> bool:
        """
        Method that checks whether the game has ended.

        If so, it returns True. Otherwise, it returns False.
        """
        for player in range(self.__num_of_players):
            if self.__boards[player].is_wall_row_full():
                return True
        return False

    def initialise_players(self, *, num_of_players: int = 2) -> list[int]:
        """
        Method that takes in the number of players, and initialises the boards.

        It then returns a list of the player indices.
        """
        # Validation to ensure the number of players is 2, 3, or 4.
        # Otherwise, a Rule Error is raised.
        if num_of_players not in (2, 3, 4):
            raise RuleError(
                {
                    "class": "Game",
                    "method": "initialise_players",
                    "message": "Azul is only designed for 2 - 4 players.",
                }
            )

        # This value is stored as an attribute.
        self.__num_of_players = num_of_players

        player_indexes: list[int] = []
        # For each player index from 0 to the number of players (-1)
        for player_index in range(num_of_players):
            # The player index is appended to the list
            player_indexes.append(player_index)
            # And a board is instantiated for each player.
            self.__boards.append(Board())

        # The list of player indexes is then returned.
        return player_indexes

    def initalise_factories(self) -> list[list[Tile]]:
        """
        Method takes in the number of players, and based on that initilialises the factories, takes the correct
        number of tiles from the bag, and then places them into the relevant factories,
        """

        # The number of factories is set to 5 if the number if players is 2,
        self.__num_of_factories: int = (
            5
            if self.__num_of_players == 2
            # and 7 if the number of players is 3.
            else 7
            if self.__num_of_players == 3
            # Otherwise it's set to 9. It's then stored as an attribute.
            else 9
        )

        # If the bag doesn't have enough tiles to be added to the factory,
        bag_tiles: list[Tile] = self.__bag.return_tile_bag()
        if len(bag_tiles) < (self.__num_of_factories * 4):
            # The tiles in the lid is added to the bag.
            self.__bag.add_tiles_to_bag(self.__lid)
            # And the lid is cleared.
            self.__lid.clear()

        # Otherwise, tiles are removed from the bag and added to the factories.
        tiles_from_bag: list[Tile] = self.__bag.remove_tiles_from_bag(
            self.__num_of_factories
        )

        # If the lid is empty, take the current contents of the factories and add them to the bag.
        current_factories: list[Tile] = []
        # For each factory,
        for factory in self.return_factories():
            # and each tile in the factory,
            for factory_tile in factory:
                # the tile is added to current factories.
                current_factories.append(factory_tile)

        # If the lid is empty,
        if not self.__lid:
            # The tiles from the current factory is added to the bag.
            self.__bag.add_tiles_to_bag(current_factories)

        # And the factory is cleared.
        self.__factory.clear_factories()

        # The factories are then added to a list,
        factories: list[list[Tile]] = self.__factory.add_tiles_to_factories(
            tiles_from_bag
        )

        # and returned.
        return factories

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
                {
                    "class": "Game",
                    "method": "select_from_factory",
                    "message": "Tile type must be a string that contains either 'black', 'ice', 'blue', 'yellow', or 'red'.",
                }
            )
        # Validation to ensure that an index isn't passed in for a factory that doesn't exist.
        if factory_index not in range(0, self.__num_of_factories):
            raise IndexError(
                {
                    "class": "Game",
                    "method": "select_from_factory",
                    "message": "You can only select a factory index with an integer from 0-3, as it only contains up to four tiles.",
                }
            )

        returned_tiles: list[list[Tile]] = []

        # A method is called on the factory object to remove all tiles of type from specified factory.
        # Which returns lists of selected and discarded tiles.
        returned_tiles = self.__factory.remove_all_instances_of_tile(
            tile_type, factory_index
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
            raise IndexError(
                {
                    "class": "Game",
                    "method": "select_from_center",
                    "message": "No Tile of this type found within the center!",
                }
            )
        if len(self.__center_of_table) <= 0:
            raise IndexError(
                {
                    "class": "Game",
                    "method": "select_from_center",
                    "message": "There are no tiles in the center of the table!",
                }
            )
        if not isinstance(tile_type, str):
            raise TypeError(
                {
                    "class": "Game",
                    "method": "select_from_center",
                    "message": "tile_type should be a string!",
                }
            )

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
        # If the "start" tile is in the center, it will be removed from the center.
        if self.__start_marker in self.__center_of_table:
            self.__center_of_table.remove(self.__start_marker)

        return selected_tiles

    def place_onto_pattern_line(
        self,
        *,
        tile_type: str,
        returned_tiles: list[list[Tile]],
        player_index: int,
        line_index: int,
    ) -> None:
        """
        Method that takes the type of tiles to be placed onto the pattern line, as well as the index of the pattern line to place the tiles onto.

        It then places the selected tiles onto the specified pattern line, and adds the discarded tiles to the center of the table.
        """
        # Validation to ensure that the type being passed in is of the specified types.
        if tile_type not in ("black", "ice", "blue", "yellow", "red"):
            raise ValueError(
                {
                    "class": "Game",
                    "method": "place_onto_pattern_line",
                    "message": "Tile type must be a string that contains either 'black', 'ice', 'blue', 'yellow', or 'red'.",
                }
            )
        # Validation that ensures an index isn't passed in for a pattern line that doesn't exist.
        if line_index not in range(0, 5):
            raise IndexError(
                {
                    "class": "Game",
                    "method": "place_onto_pattern_line",
                    "message": "Selected Pattern Line doesn't exist. Please provide an index from 0-4.",
                }
            )
        if len(returned_tiles) <= 0:
            raise IndexError(
                {
                    "class": "Game",
                    "method": "place_onto_pattern_line",
                    "message": "Tile list provided is empty!",
                }
            )

        selected_tiles: list[Tile] = returned_tiles[0]
        discarded_tiles: list[Tile] = returned_tiles[1]

        # If tile already exists at the line index on the wall, an error is raised.
        if self.__boards[player_index].is_tile_on_wall(line_index, tile_type):
            raise RuleError(
                {
                    "class": "Game",
                    "method": "place_onto_pattern_line",
                    "message": "Tile already exists on the wall! Cannot add to this pattern line.",
                }
            )

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
            # Validation to ensure that each tile in the list is a valid tile, including the start marker.
            if tile not in ("black", "ice", "blue", "yellow", "red", "start"):
                raise ValueError(
                    {
                        "class": "Game",
                        "method": "place_onto_floor_line",
                        "message": "Tile type must be a string that contains either 'black', 'ice', 'blue', 'yellow', 'red', or 'start'.",
                    }
                )
        # If the length of the tiles list is less than 0, throw an index error.
        if len(tiles) <= 0:
            raise IndexError(
                {
                    "class": "Game",
                    "method": "place_onto_floor_line",
                    "message": "List provided is empty!",
                }
            )
        # The tiles in the list are then added to the floor line.
        returned_tiles: list[Tile] | None = self.__boards[
            player_index
        ].place_tiles_onto_floor_line(tiles=tiles)
        # If there are returned tiles, that means the floor line is full.
        # And the leftover tiles are added to the lid.
        if returned_tiles is not None:
            for tile in returned_tiles:
                self.__lid.append(tile)

    def place_onto_wall(self, *, player_index: int) -> None:
        """
        Method that takes the line index and player index, and places the tile onto the wall.

        It then stores the list of tiles from the cleared pattern lines into the lid.
        """

        # Validation to ensure that the center of the table is empty. If it isn't it raises a Rule Error.
        if len(self.__center_of_table) > 0:
            raise RuleError(
                {
                    "class": "Game",
                    "method": "place_onto_wall",
                    "message": "Cannot place onto the wall while the center still has tiles!",
                }
            )
        # Similarly, if the factories aren't empty, it raises a Rule Error.
        if not self.__factory.is_factories_empty():
            raise RuleError(
                {
                    "class": "Game",
                    "method": "place_onto_wall",
                    "message": "Cannot place onto the wall while the factories still have tiles!",
                }
            )

        # For the selected player, the tiles on their full pattern lines are added to the wall. The cleared pattern lines are then returned.
        returned_tiles: list[list[Tile]] = self.__boards[
            player_index
        ].place_tiles_onto_wall()

        # And for each cleared pattern line,
        for cleared_line in returned_tiles:
            # as long as the line isn't empty,
            if len(cleared_line) > 0:
                # the tiles in the line are added to the lid.
                self.__lid += cleared_line

    def calculate_final_scores(self) -> list[int]:
        """
        Method that iterates through the number of players, and then adds them to the final scores.

        It then returns the final scores.
        """
        # For each player, calculate their final score and add it to final scores.
        final_scores: list[int] = [
            self._calculate_final_score(player_index=player_index)
            for player_index in range(self.__num_of_players)
        ]

        # The final score attribute is incremented by final score,
        self.__final_scores += final_scores
        # and then returned.
        return final_scores
