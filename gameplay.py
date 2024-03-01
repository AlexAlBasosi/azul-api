"""
This file contains the implementation that sets the game's parameters and plays the game.
"""

# This script simulates setting up the game and simulating a user's actions as they play the game.

from random import randrange
import logging
from game import Game
from game import Tile
from game import RuleError

game: Game = Game()

def get_available_pattern_line_index(returned_tiles: list[list[Tile]],
tile_type: str, selected_player_index: int) -> int | None:
    """
    Method that takes in the tiles returned from the select_from_factory method and checks if there are available spaces in the pattern line.

    It then returns the index of that method.
    """
    print(f"Returned Tiles: {returned_tiles[0]}")
    tiles_length: int = len(returned_tiles[0])
    pattern_lines: list[list[Tile]] = game.return_pattern_lines(player_index=selected_player_index)
    pattern_line_index: int | None = None
    for index in range(5):
        pattern_line_capacity = index + 1
        pattern_line_availability = pattern_line_capacity - len(pattern_lines[index])
        if not game.is_tile_on_wall(line_index=index, tile_type=tile_type, player_index=selected_player_index):
            if len(pattern_lines[index]) == 0:
                if tiles_length <= pattern_line_availability:
                    return index
            if tiles_length <= pattern_line_availability and pattern_lines[index][-1] == tile_type:
                pattern_line_index = index
    return pattern_line_index
        

def play_turn_factory(selected_player_index: int, factory_index: int) -> None:
    """
    Method that takes in the player_index and factory_index and selects tiles from the specified factory and places them onto the pattern line.
    """
    ## Now, the user starts to play. They start by selecting all the red tiles from the first factory.
    tile = str(factories[factory_index][randrange(0, 3)])
    tiles = game.select_from_factory(tile_type=tile, factory_index=factory_index)

    # The returned tiles, which include the selected and discarded tiles, are passed into this method.
    # Here, the user places the tiles onto the second pattern line.

    available_index: int | None = get_available_pattern_line_index(tiles, tile, selected_player_index)
    if available_index is not None:
        game.place_onto_pattern_line(tile_type=tile, returned_tiles=tiles, player_index=selected_player_index, line_index=available_index)
    else:
        game.place_onto_floor_line(tiles=tiles[0], player_index=selected_player_index)

    print(f"\nPlayer {selected_player_index+1}:\n")
    print(f"Factories: {game.return_factories()}")
    print(f"Pattern Lines: {game.return_pattern_lines(player_index=selected_player_index)}")
    print(f"Center: {game.return_center()}")
    print(f"Floor Line: {game.return_floor_line(player_index=selected_player_index)}")

    print("\n\n")

def play_turn_center(selected_player_index: int) -> None:
    """
    Method that takes in the player_index and line_index and selects tiles from the center and places them onto the pattern line.
    """
    
    tile = str(game.return_center()[0]) if game.return_center()[0] != "start" else str(game.return_center()[1])
    tiles: list[list[Tile]] = [game.select_from_center(tile_type=tile, player_index=selected_player_index), []]

    available_index: int | None = get_available_pattern_line_index(tiles, tile, selected_player_index)

    if available_index is not None:
        game.place_onto_pattern_line(tile_type=tile, returned_tiles=tiles, player_index=selected_player_index, line_index=available_index)
    else:
        game.place_onto_floor_line(tiles=tiles[0], player_index=selected_player_index)

    print(f"\nPlayer {selected_player_index+1}:\n")
    print(f"Factories: {game.return_factories()}")
    print(f"Pattern Lines: {game.return_pattern_lines(player_index=selected_player_index)}")
    print(f"Center: {game.return_center()}")
    print(f"Floor Line: {game.return_floor_line(player_index=selected_player_index)}")
    print("\n\n")

def play_factory_turns() -> None:
    """
    Method that loops through each factory and alternates between the number of players, each taking tiles from a factory.
    """
    selected_player: int = 0

    for factory_index in range(game.return_num_of_factories()):
        play_turn_factory(selected_player, factory_index)
        selected_player = (selected_player + 1) % game.return_num_of_players()

def play_center_turns() -> None:
    """
    Method that, while center is not empty, alternates between players, each taking from the center until the center is empty.
    """
    selected_player: int = 0

    while not game.is_center_empty():
        play_turn_center(selected_player)
        selected_player = (selected_player + 1) % game.return_num_of_players()

def place_tiles_onto_wall() -> None:
    """
    Method that loops through each player, and for each player places the tiles from each pattern line onto the wall.
    """
    for player in players:
        game.place_onto_wall(player_index=player)

        print(f"\nPlayer {player+1}:\n")
        wall: list[list[list[str | Tile | None]]] = game.return_wall(player_index=player)
        for wall_row in wall:
            print(f"{wall_row}\n")
        print(f"Score: {game.return_score(player_index=player)}\n")

        print(f"Pattern Lines: {game.return_pattern_lines(player_index=player)}")
        print(f"Lid: {game.return_lid()}\n")
    print("\n\n")

def format_exception_message(exception: Exception, exception_type: str) -> str:
    """
    Method that takes in the exception message and the type of exception, and returns a formatted string to be logged as an error.
    """
    exception_message_formatted: str = f"{exception_type}Error\n Class: {exception.args[0]["class"]}\n Method: {exception.args[0]["method"]}\n Message: {exception.args[0]["message"]}"

    return exception_message_formatted

try:
    # Game Setup:
    ## This phase involves setting up the game and initialising the factories. 

    players: list[int] = game.initialise_players(num_of_players = 2)
    factories: list[list[Tile]] = []
    center: list[Tile | str] = game.return_center()

    print(f"Factories: {game.return_factories()}")
    print(f"Center: {game.return_center()}")
    print(f"Lid: {game.return_lid()}\n\n")

    round_index: int = 0
    while not game.is_game_ended():
        factories = game.initalise_factories()
        if not factories:
            break

        print(f"Round {round_index+1}: \n\n")

        ## Factory Offer:
        print("Taking from factories:\n\n")
        play_factory_turns()

        print("Now taking from center:\n\n")
        play_center_turns()
        
        ## Wall Tiling
        # Now, the user starts to place tiles onto the wall from the pattern lines.
        place_tiles_onto_wall()

        print("\n\n")
        round_index += 1

    print("Game ended!\n")

    player_scores: list[int] = game.calculate_final_scores()
    for player_index, player_score in enumerate(player_scores):
        print(f"Player {player_index + 1} Score: {player_score}")

    winners: dict[int, int] = game.return_winners()
    winner_indexes: list[int] = list(winners.keys())
    if len(winners) == 1:
        winner_index = winner_indexes[0]
        print(f"\nPlayer {winner_index + 1} wins!\n")
    else:
        print("\nIts a tie! The winners are:\n")
        for winner_index in winner_indexes:
            print(f"Player {winner_index + 1} Score: {winners[winner_index]}")

# The errors raised are handled here, which are printed onto the console.
# In a production environment these would be added to a logger.
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

# TODO: Add comments in various functions
# TODO: Update README
