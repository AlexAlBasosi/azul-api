"""
This file contains the implementation that sets the game's parameters and plays the game.
"""

# This script simulates setting up the game and simulating a user's actions as they play the game.

# Please note, the script doesn't play the game very well,
# so the simulated scores are horribly low. :D

from random import randrange
import logging
from game import Game
from game import Tile
from game import RuleError

game: Game = Game()

def get_available_pattern_line_index(returned_tiles: list[list[Tile]],
tile_type: str, selected_player_index: int) -> int | None:
    """
    Method that takes in the tiles returned from the select_from_factory method 
    and checks if there are available spaces in the pattern line.

    It then returns the index of that method.
    """
    print(f"Returned Tiles: {returned_tiles[0]}")
    # The tiles to be added to the floor line are stored in the first sub-list.
    tiles_length: int = len(returned_tiles[0])
    # The pattern lines for the selected user is stored into pattern_lines.
    pattern_lines: list[list[Tile]] = game.return_pattern_lines(player_index=selected_player_index)
    # The selected pattern line index is initially set to None.
    pattern_line_index: int | None = None
    # For each pattern line index from 0 - 4
    for index in range(5):
        # The pattern line capacity is index + 1, for example, the first pattern line's capacity is 1, and then second is 2, etc.
        pattern_line_capacity = index + 1
        # The availability is the capacity - how many tiles are actually on the line.
        pattern_line_availability = pattern_line_capacity - len(pattern_lines[index])
        # As long as the tile on the corresponding index of the wall isn't full
        if not game.is_tile_on_wall(line_index=index, tile_type=tile_type, player_index=selected_player_index):
            # If there are no tiles in the selected pattern line
            if len(pattern_lines[index]) == 0:
                # and the number of tiles is less than or equal to the available space in the pattern line
                if tiles_length <= pattern_line_availability:
                    # then this line index is returned as an available index
                    return index
            # If the number of tiles is less than or equal to the available space in the pattern line but not zero (there are tiles on the line)
            # and they're of the same type as the tiles in the list
            if tiles_length <= pattern_line_availability and pattern_lines[index][-1] == tile_type:
                # then this pattern line is returned as an available index
                pattern_line_index = index
    return pattern_line_index

def play_turn_factory(selected_player_index: int, factory_index: int) -> None:
    """
    Method that takes in the player_index and factory_index and selects tiles from the specified factory and places them onto the pattern line.
    """
    # Now, the user starts to play. They start by selecting a random tile index (from 0 to 3) from the selected factory index.
    tile: str = str(factories[factory_index][randrange(0, 3)])

    # The below method returns a list which contains two lists: tile(s) selected from the factory, and tiles to be discarded to the center of the table.
    tiles: list[list[Tile]] = game.select_from_factory(tile_type=tile, factory_index=factory_index)

    # Here, the user places the tiles onto the second pattern line.

    # This method then checks if there are any pattern lines available for the selected tiles to be placed on.
    available_index: int | None = get_available_pattern_line_index(tiles, tile, selected_player_index)
    if available_index is not None:
        # If there is, then those tiles are placed onto the pattern line to this method, passing in the tile type, the returned tiles, the index of the player, and the pattern line index.
        game.place_onto_pattern_line(tile_type=tile, returned_tiles=tiles, player_index=selected_player_index, line_index=available_index)
    else:
        # However, if there are no available pattern lines, then the tiles are added to the floor line.
        game.place_onto_floor_line(tiles=tiles[0], player_index=selected_player_index)

    print(f"\nPlayer {selected_player_index+1}:\n")
    # The factories are returned.
    print(f"Factories: {game.return_factories()}")
    # The pattern lines are returned.
    print(f"Pattern Lines: {game.return_pattern_lines(player_index=selected_player_index)}")
    # The center is returned.
    print(f"Center: {game.return_center()}")
    # The floor line is returned.
    print(f"Floor Line: {game.return_floor_line(player_index=selected_player_index)}")

    print("\n\n")

def play_turn_center(selected_player_index: int) -> None:
    """
    Method that takes in the player_index and line_index and selects tiles from the center and places them onto the pattern line.
    """
    # If the returned tiles contains the start tile, then tile type becomes the tile at the 1st index, otherwise it's the type at the 0th index.
    tile = str(game.return_center()[0]) if game.return_center()[0] != "start" else str(game.return_center()[1])
    # The user selects from the center, and the returned tiles are stored in tiles.
    tiles: list[list[Tile]] = [game.select_from_center(tile_type=tile, player_index=selected_player_index), []]

    # This method then checks if there are any pattern lines available for the selected tiles to be placed on.
    available_index: int | None = get_available_pattern_line_index(tiles, tile, selected_player_index)

    # If there are, then the tiles are placed onto the pattern line at the selected line index for the selected player.
    if available_index is not None:
        game.place_onto_pattern_line(tile_type=tile, returned_tiles=tiles, player_index=selected_player_index, line_index=available_index)
    # Otherwise, the tiles are placed onto the floor line.
    else:
        game.place_onto_floor_line(tiles=tiles[0], player_index=selected_player_index)

    print(f"\nPlayer {selected_player_index+1}:\n")
    # The factories are returned.
    print(f"Factories: {game.return_factories()}")
    # The pattern lines are returned.
    print(f"Pattern Lines: {game.return_pattern_lines(player_index=selected_player_index)}")
    # The center is returned.
    print(f"Center: {game.return_center()}")
    # The floor line is returned.
    print(f"Floor Line: {game.return_floor_line(player_index=selected_player_index)}")
    print("\n\n")

def play_factory_turns() -> None:
    """
    Method that loops through each factory and alternates between the number of players, each taking tiles from a factory.
    """
    selected_player: int = 0

    # For each factory, a turn is played for the selected player.
    for factory_index in range(game.return_num_of_factories()):
        play_turn_factory(selected_player, factory_index)

        # The next player is selected by adding 1 to the selected player then modding by the total number of players.
        # For instance, if there are two players, it will be:
            # 0 + 1 % 2 = 1
            # 1 + 1 % 2 = 0, and so on.
        selected_player = (selected_player + 1) % game.return_num_of_players()

def play_center_turns() -> None:
    """
    Method that, while center is not empty, alternates between players, each taking from the center until the center is empty.
    """
    selected_player: int = 0

    # For each player, they will take turns selecting from the center until the center is empty.
    while not game.is_center_empty():
        play_turn_center(selected_player)
        selected_player = (selected_player + 1) % game.return_num_of_players()

def place_tiles_onto_wall() -> None:
    """
    Method that loops through each player, and for each player places the tiles from each pattern line onto the wall.
    """
    # For each player in the list of players.
    for player in players:
        # The player places the tiles that have a full pattern line onto the wall.
        game.place_onto_wall(player_index=player)

        print(f"\nPlayer {player+1}:\n")
        # The wall is returned.
        wall: list[list[list[str | Tile | None]]] = game.return_wall(player_index=player)
        for wall_row in wall:
            print(f"{wall_row}\n")
        # The score is returned.
        print(f"Score: {game.return_score(player_index=player)}\n")
        # The pattern lines are returned.
        print(f"Pattern Lines: {game.return_pattern_lines(player_index=player)}")
        # The lid is returned.
        print(f"Lid: {game.return_lid()}\n")
    print("\n\n")

def format_exception_message(exception: Exception, exception_type: str) -> str:
    """
    Method that takes in the exception message and the type of exception, and returns a formatted string to be logged as an error.
    """
    exception_message_formatted: str = ""
    # If the error received is in the format we expect, as a dict, then it's formatted accordingly.
    if isinstance(exception.args[0], dict):
        # The returned error message contains the type of error, as well as the class and method in which the error was raised.
        exception_message_formatted = f"{exception_type}Error\n Class: {exception.args[0]["class"]}\n Method: {exception.args[0]["method"]}\n Message: {exception.args[0]["message"]}"
    else:
        # Otherwise, it's stringified and logged to the console as is.
        exception_message_formatted = str(exception)

    # The formatted exception message is then returned.
    return exception_message_formatted

try:
    # Game Setup:
    ## This phase involves setting up the game and initialising the factories and players.

    # The players are initialised. Here, we're setting the number of players to 2.
    # Can also be set to 3 or 4. It's set to 2 if nothing is passed.
    players: list[int] = game.initialise_players(num_of_players = 2)
    factories: list[list[Tile]] = []
    # The center is returned.
    center: list[Tile | str] = game.return_center()

    print(f"Factories: {game.return_factories()}")
    print(f"Center: {game.return_center()}")
    print(f"Lid: {game.return_lid()}\n\n")

    ## First, the round index is set to 0.
    round_index: int = 0
    ## While the game isn't ended, a while loop is executed, playing a number of rounds for each player.
    while not game.is_game_ended():
        # The factories are initialised.
        factories = game.initalise_factories()
        if not factories:
            break

        print(f"Round {round_index+1}: \n\n")

        # Factory Offer:
        print("Taking from factories:\n\n")
        ## This method plays a turn for each player until the factories are empty.
        play_factory_turns()

        print("Now taking from center:\n\n")
        ## This method plays a turn for each player until the center is empty.
        play_center_turns()
        
        ## Wall Tiling
        # Now that both the factories and center is empty, the players start to place tiles onto the wall from the pattern lines.
        place_tiles_onto_wall()

        print("\n\n")
        round_index += 1

    print("Game ended!\n")

    # The player scores are calculated.
    player_scores: list[int] = game.calculate_final_scores()
    for player_index, player_score in enumerate(player_scores):
        print(f"Player {player_index + 1} Score: {player_score}")

    # The winners are then returned.
    winners: dict[int, int] = game.return_winners()
    winner_indexes: list[int] = list(winners.keys())
    # If the length of the winners dict is 1, then a message is printed with the winner and their score.
    if len(winners) == 1:
        winner_index = winner_indexes[0]
        print(f"\nPlayer {winner_index + 1} wins!\n")
    # Otherwise, it's a tie, and their scores are printed.
    else:
        print("\nIts a tie! The winners are:\n")
        for winner_index in winner_indexes:
            print(f"Player {winner_index + 1} Score: {winners[winner_index]}")

# The errors raised are handled here, which are then logged according to the type of error. This also prints the error message to the console.
except RuleError as rule_message:
    rule_exception_message: str = format_exception_message(rule_message, "Rule")
    logging.error(rule_exception_message)
except ValueError as value_message:
    value_exception_message: str = format_exception_message(value_message, "Value")
    logging.error(value_exception_message)
except IndexError as index_message:
    index_exception_message: str = format_exception_message(index_message, "Index")
    logging.error(index_exception_message)
except TypeError as type_message:
    type_exception_message: str = format_exception_message(type_message, "Type")
    logging.error(type_exception_message)
except OverflowError as overflow_message:
    overflow_exception_message: str = format_exception_message(overflow_message, "Overflow")
    logging.error(overflow_exception_message)

# TODO: Update README
