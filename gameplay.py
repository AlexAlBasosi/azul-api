"""
This file contains the implementation that sets the game's parameters and plays the game.
"""

# This script simulates setting up the game and simulating a user's actions as they play the game.

from game import Game
from game import Tile
from random import randrange

game: Game = Game()

def get_available_pattern_line_index(returned_tiles: list[list[Tile]],
tile_type: str, player_index: int) -> int | None:
    """
    Method that takes in the tiles returned from the select_from_factory method and checks if there are available spaces in the pattern line.

    It then returns the index of that method.
    """
    print(f"Returned Tiles: {returned_tiles[0]}")
    tiles_length: int = len(returned_tiles[0])
    pattern_lines: list[list[Tile]] = game.return_pattern_lines(player_index=player_index)
    pattern_line_index: int | None = None
    for index in range(5):
        pattern_line_capacity = index + 1
        pattern_line_availability = pattern_line_capacity - len(pattern_lines[index])
        if not game.is_tile_on_wall(line_index=index, tile_type=tile_type, player_index=player_index):
            if len(pattern_lines[index]) == 0:
                if tiles_length <= pattern_line_availability:
                    return index
            if tiles_length <= pattern_line_availability and pattern_lines[index][-1] == tile_type:
                pattern_line_index = index
    return pattern_line_index
        

def play_turn_factory(player_index: int, factory_index: int) -> None:
    """
    Method that takes in the player_index and factory_index and selects tiles from the specified factory and places them onto the pattern line.
    """
    ## Now, the user starts to play. They start by selecting all the red tiles from the first factory.
    tile = str(factories[factory_index][randrange(0, 3)])
    tiles = game.select_from_factory(tile_type=tile, factory_index=factory_index)

    # The returned tiles, which include the selected and discarded tiles, are passed into this method.
    # Here, the user places the tiles onto the second pattern line.

    available_index: int | None = get_available_pattern_line_index(tiles, tile, player_index)
    if available_index is not None:
        game.place_onto_pattern_line(tile_type=tile, returned_tiles=tiles, player_index=player_index, line_index=available_index)
    # else:
    #     game.place_onto_floor_line(tiles=tiles[0], player_index=player_index)

    print(f"\nPlayer {player_index+1}:\n")
    print(f"Factories: {game.return_factories()}")
    print(f"Pattern Lines: {game.return_pattern_lines(player_index=player_index)}")
    print(f"Center: {game.return_center()}")
    print(f"Floor Line: {game.return_floor_line(player_index=player_index)}")

    print("\n\n")

def play_turn_center(player_index: int) -> None:
    """
    Method that takes in the player_index and line_index and selects tiles from the center and places them onto the pattern line.
    """
    
    tile = str(game.return_center()[0]) if game.return_center()[0] != "start" else str(game.return_center()[1])
    tiles: list[list[Tile]] = [game.select_from_center(tile_type=tile, player_index=player_index), []]

    available_index: int | None = get_available_pattern_line_index(tiles, tile, player_index)

    if available_index is not None:
        game.place_onto_pattern_line(tile_type=tile, returned_tiles=tiles, player_index=player_index, line_index=available_index)
    # else:
    #     game.place_onto_floor_line(tiles=tiles[0], player_index=player_index)

    print(f"\nPlayer {player_index+1}:\n")
    print(f"Factories: {game.return_factories()}")
    print(f"Pattern Lines: {game.return_pattern_lines(player_index=player_index)}")
    print(f"Center: {game.return_center()}")
    print(f"Floor Line: {game.return_floor_line(player_index=player_index)}")
    print("\n\n")

def play_factory_turns() -> None:
    """
    Method that loops through each factory and alternates between the number of players, each taking tiles from a factory.
    """
    player_index: int = 0

    for factory_index in range(game.return_num_of_factories()):
        play_turn_factory(player_index=player_index, factory_index=factory_index)
        player_index = (player_index + 1) % game.return_num_of_players()

def play_center_turns() -> None:
    """
    Method that, while center is not empty, alternates between players, each taking from the center until the center is empty.
    """
    player_index: int = 0

    while not game.is_center_empty():
        play_turn_center(player_index=player_index)
        player_index = (player_index + 1) % game.return_num_of_players()

def place_tiles_onto_wall() -> None:
    """
    Method that loops through each player, and for each player places the tiles from each pattern line onto the wall.
    """
    for player_index in players:
        game.place_onto_wall(player_index=player_index)

        print(f"\nPlayer {player_index+1}:\n")
        wall: list[list[list[str | Tile | None]]] = game.return_wall(player_index=player_index)
        for wall_row in wall:
            print(f"{wall_row}\n")
        print(f"Score: {game.return_score(player_index=player_index)}\n")

        print(f"Pattern Lines: {game.return_pattern_lines(player_index=player_index)}")
        print(f"Lid: {game.return_lid()}\n")
    print("\n\n")

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

    print("Game ended!")
        
    

# The errors raised are handled here, which are printed onto the console. In a production environment these would be added to a logger.
except ValueError as value_message:
    print(f"Value Error: {value_message}")
except IndexError as index_message:
    print(f"Index Error: {index_message}")
except TypeError as type_message:
    print(f"Type Error: {type_message}")
except OverflowError as overflow_message:
    print(f"Overflow Error: {overflow_message}")

# TODO: if bag is empty, refill from lid
# TODO: if 5 consecutive horizontal tiles, end game.
# TODO: add final scores
# TODO: refactor select from* methods to be play_turn*
# TODO: look into adding a logger
    
# TODO: Add positional arguments to all public methods
# TODO: Add validation to all public methods.
# TODO: Add comments in various functions
# TODO: Refactor error message to include class and method where error was raised.
    # TODO: add RuleError for things that violate game rules
