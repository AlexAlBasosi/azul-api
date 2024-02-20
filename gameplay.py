"""
This file contains the implementation that sets the game's parameters and plays the game.
"""

# This script simulates setting up the game and simulating a user's actions as they play the game.

from game import Game
from game import Tile

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
        if len(pattern_lines[index]) == 0:
            if(tiles_length <= pattern_line_availability):
                pattern_line_index = index
        elif pattern_lines[index][-1] == tile_type:
            if tiles_length <= pattern_line_availability:
                pattern_line_index = index
    return pattern_line_index
        

def play_turn_factory(player_index: int, factory_index: int) -> None:
    """
    Method that takes in the player_index and factory_index and selects tiles from the specified factory and places them onto the pattern line.
    """
    ## Now, the user starts to play. They start by selecting all the red tiles from the first factory.
    tile = str(factories[factory_index][0])
    tiles = game.select_from_factory(tile_type=tile, factory_index=factory_index)

    # The returned tiles, which include the selected and discarded tiles, are passed into this method.
    # Here, the user places the tiles onto the second pattern line.

    available_index: int | None = get_available_pattern_line_index(tiles, tile, player_index)
    print(f"available index: {available_index}")
    if available_index is not None:
        game.place_onto_pattern_line(tile_type=tile, returned_tiles=tiles, player_index=player_index, line_index=available_index)

    print(f"\nPlayer {player_index+1}:\n")
    print(f"Factories: {game.return_factories()}")
    print(f"Pattern Lines: {game.return_pattern_lines(player_index=player_index)}")
    print(f"Center: {game.return_center()}")
    print(f"Floor Line: {game.return_floor_line(player_index=player_index)}")

    print("\n\n")

def play_turn_center(player_index: int, line_index: int) -> None:
    """
    Method that takes in the player_index and line_index and selects tiles from the center and places them onto the pattern line.
    """
    
    # print(f"Center 1: {game.return_center()[1]}")
    tile = str(game.return_center()[0]) if game.return_center()[0] != "start" else str(game.return_center()[1])
    tiles: list[list[Tile]] = [game.select_from_center(tile_type=tile, player_index=player_index), []]

    game.place_onto_pattern_line(tile_type=tile, returned_tiles=tiles, player_index=player_index, line_index=line_index)

    print(f"\nPlayer {player_index+1}:\n")
    print(f"Factories: {game.return_factories()}")
    print(f"Pattern Lines: {game.return_pattern_lines(player_index=0)}")
    print(f"Center: {game.return_center()}")
    print(f"Floor Line: {game.return_floor_line(player_index=player_index)}")
    print("\n\n")

try:
    # Game Setup:
    ## This phase involves setting up the game and initialising the factories. 

    players: list[int] = game.initialise_players(num_of_players = 2)
    factories: list[list[Tile]] = game.initalise_factories()
    center: list[Tile | str] = game.return_center()

    player_1: int = players[0]
    player_2: int = players[1]

    print(f"Factories: {game.return_factories()}")
    print(f"Center: {game.return_center()}")
    print(f"Lid: {game.return_lid()}\n")

    # Factory Offer:
    play_turn_factory(player_index=0, factory_index=0)

    play_turn_factory(player_index=1, factory_index=1)

    play_turn_factory(player_index=0, factory_index=2)

    play_turn_factory(player_index=1, factory_index=3)

    play_turn_factory(player_index=0, factory_index=4)

    # play_turn_center(player_index=1, line_index=2)
    # play_turn_center(player_index=0, line_index=3)
    # play_turn_center(player_index=1, line_index=4)
    # play_turn_center(player_index=0, line_index=1)

    # TODO: refactor this so that the user clears the center organically.
    game.clear_center()
    print(f"Center of Table: {game.return_center()}")
    print(f"Floor Line: {game.return_floor_line(player_index=0)}\n")
    
    print("\n\n")

    # Wall Tiling
    ## Now, the user starts to place tiles onto the wall from the pattern lines.
    # print(f"Wall: {game.return_wall(player_index=0)}")
    # game.place_onto_wall(line_index=0, player_index=0)
    # print(f"Wall: {game.return_wall(player_index=0)}")



except ValueError as value_message:
    print(f"Value Error: {value_message}")
except IndexError as index_message:
    print(f"Index Error: {index_message}")
except TypeError as type_message:
    print(f"Type Error: {type_message}")
except OverflowError as overflow_message:
    print(f"Overflow Error: {overflow_message}")

# TODO: refactor main script into functions to simplify
    # TODO: Refactor select from center to use available index method
    # TODO: Refactor play_turn_factory to be a loop that ends when factories are empty
    # TODO: Refactor play_turn center to be a loop that ends when center is empty
# TODO: Wall scoring
# TODO: if factories are empty, refill from bag
# TODO: if bag is empty, refill from lid
    
# TODO: Look into fixing overflow issues -> build script that checks pattern lines.
# TODO: Add positional arguments to all public methods
# TODO: Add validation to all public methods.
# TODO: Add comments in various functions
# TODO: Refactor error message to include class and method where error was raised.